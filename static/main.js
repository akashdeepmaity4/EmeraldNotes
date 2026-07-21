document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (darkModeToggle) darkModeToggle.checked = true;
    }

    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', () => {
            if (darkModeToggle.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // --- Live Parser & Project Saver ---
    const rawInput = document.getElementById('rawInput');
    const parsedOutput = document.getElementById('parsedOutput');
    const saveBtn = document.getElementById('saveBtn');
    const filenameInput = document.getElementById('filenameInput');

    if (rawInput && parsedOutput) {
        const updatePreview = () => {
            const text = rawInput.value;
            
            fetch('/api/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            })
            .then(res => res.json())
            .then(data => {
                parsedOutput.innerHTML = data.html;
            })
            .catch(err => console.error('Parsing error:', err));
        };

        // Render initially on load and then on input change
        updatePreview();
        rawInput.addEventListener('input', updatePreview);
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const filename = filenameInput.value.trim();
            const content = rawInput.value;

            if (!filename) {
                alert('Please enter a project name.');
                return;
            }

            fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename: filename, content: content })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('Project saved successfully!');
                    window.location.href = `/edit/${data.filename}`;
                } else {
                    alert(data.error || 'Failed to save project.');
                }
            })
            .catch(err => console.error('Saving error:', err));
        });
    }
});