param(
    [string]$MsiPath = "dist\VeritasNotes*.msi",
    [string]$TimestampServer = "http://digicert.com",
    [string]$Base64Certificate = "",
    [string]$CertificatePassword = ""
)

Write-Host "=== Veritas Notes MSI Signing Script ===" -ForegroundColor Cyan
Write-Host ""

# 1. Find the MSI file
$msiFiles = Get-ChildItem -Path $MsiPath -ErrorAction SilentlyContinue
if (-not $msiFiles) {
    Write-Host "ERROR: No MSI file found matching pattern: $MsiPath" -ForegroundColor Red
    exit 1
}

$msiFile = $msiFiles[0].FullName
Write-Host "Found MSI file: $msiFile" -ForegroundColor Green

# 2. Acquire the Code Signing Certificate
$cert = $null
$tempCertPath = $null

if (-not [string]::IsNullOrWhiteSpace($Base64Certificate)) {
    # CI/CD Mode: Loading certificate from GitHub Secrets text
    Write-Host "CI/CD Context Detected: Loading certificate from base64 environment variable..." -ForegroundColor Cyan
    try {
        $certBytes = [System.Convert]::FromBase64String($Base64Certificate)
        $tempCertPath = Join-Path $env:TEMP "temp_signing_cert.pfx"
        [System.IO.File]::WriteAllBytes($tempCertPath, $certBytes)
        
        $secPassword = ConvertTo-SecureString $CertificatePassword -AsPlainText -Force
        $cert = Get-PfxCertificate -FilePath $tempCertPath -Password $secPassword
    } catch {
        Write-Host "ERROR: Failed to decode or parse the provided base64 certificate!" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
} else {
    # Local Mode: Loading certificate from your Windows User Certificate Store
    Write-Host "Local Context Detected: Searching local Windows User Certificate Store..." -ForegroundColor Cyan
    $cert = Get-ChildItem -Path Cert:\CurrentUser\My | 
        Where-Object { $_.Subject -like "*Veritas Notes*" -and $_.EnhancedKeyUsageList.FriendlyName -contains "Code Signing" } |
        Select-Object -First 1
}

if (-not $cert) {
    Write-Host "ERROR: No Veritas Notes code signing certificate could be loaded!" -ForegroundColor Red
    Write-Host "Locally, run the following to recreate one if needed:" -ForegroundColor Yellow
    Write-Host '  New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=Veritas Notes, O=Akash Deep Maity, C=IN" -CertStoreLocation "Cert:\CurrentUser\My" -NotAfter (Get-Date).AddYears(2)' -ForegroundColor Yellow
    exit 1
}

Write-Host "Using certificate:" -ForegroundColor Green
Write-Host "  Subject: $($cert.Subject)"
Write-Host "  Thumbprint: $($cert.Thumbprint)"
Write-Host "  Expires: $($cert.NotAfter)"
Write-Host ""

# 3. Sign the MSI file
Write-Host "Signing MSI file..." -ForegroundColor Cyan
try {
    $result = Set-AuthenticodeSignature -FilePath $msiFile -Certificate $cert -TimestampServer $TimestampServer
    
    if ($result.Status -eq "Valid" -or $result.Status -eq "UnknownError") {
        Write-Host "MSI file signed successfully!" -ForegroundColor Green
        Write-Host "  Status: $($result.Status)"
        Write-Host "  Path: $($result.Path)"
        Write-Host ""
        
        if ($result.Status -eq "UnknownError") {
            Write-Host "Note: Status shows 'UnknownError'. This is normal for self-signed certificates or environments missing root trust chains." -ForegroundColor Yellow
        }
    } else {
        Write-Host "WARNING: Signing completed with status: $($result.Status)" -ForegroundColor Yellow
        Write-Host "  Message: $($result.StatusMessage)"
    }
} catch {
    Write-Host "ERROR: Failed to sign MSI file!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
} finally {
    if ($tempCertPath -and (Test-Path $tempCertPath)) {
        Remove-Item $tempCertPath -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "=== Signing Complete ===" -ForegroundColor Cyan
