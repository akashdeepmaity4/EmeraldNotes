# EMERALD NOTES
Emerald Notes is ultra-lightweight standard text editor, weighting a mere 18 MB and taking only 5-10 MB RAM during active use. It allows you to create and edit text files. It is fully local, keeping your files 100% safe inside your own local storage. It also supports native Markdown file formatting using the custom GUI formatting toolbar. 

![techstack](https://img.shields.io/badge/Python-blue)
![techstack](https://img.shields.io/badge/Bash-green)
![techstack](https://img.shields.io/badge/JavaScript-yellow)
![techstack](https://img.shields.io/badge/HTML-5-orange)
![techstack](https://img.shields.io/badge/CSS-3-blue)
![Electron](https://img.shields.io/badge/electron-39.1.2-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-2.0-brightgreen)

## MUST DO

1. Open the 'remakeexecutable.sh' file in an IDE or text editor and change line 2 to the location where you want the root directory to be. 
1. Make sure it is the same path as the parent codebase to avoid errors.
1. install dependencies using the 'requirements.txt' file. [Refer to line 44]
<br>
<br>
<br>

![logo](static/emeraldnoteslogo.png)



## HIGHLIGHTS

1. It is completely local, meaning you can access your files at any time
1. It is very lightweight, suitable for mobile devices or low-end computers.
1. Can be locally run on all major OSs, but .exe application can ONLY be run on windows.



## FEATURES

- Markdown formatting support with GUI formatting toolbar
- .exe app, localhost webapp AND local webapp using Pywebview
- Native Dark mode support throughout the app



## How to Use

1. Download the codebase to a directory named 'emeraldnotes'. This will act as the root directory.
1. Open 'remakeexecutable.sh' and change line 2 to the location of emeraldnotes root directory. 
1. Run 'remakeexecutable.sh' via Bash to make a safe application.

### OR

1. Download the codebase to a directory named 'emeraldnotes'. This will act as the root directory.
1. Run 'launcher.py' via python in Command Prompt/ Bourne Again Shell (Bash).
1. This opens a native webapp.

### OR

1. Download the codebase to a directory named 'emeraldnotes'. This will act as the root directory.
1. Run 'app/app.py' via python.
1. Navigate to http://localhost:5000 in your browser.



## Dependencies

- Python 3.x (3.14 recommended)
- Bash (To automate the application making process. Highly recommended)
- Flask (Non-Negotiable to run the app)
- pyinstaller (If you want .exe application)
- pywebview (If you want to run the Webapp natively)



### Install Dependencies

```
pip install -r requirements.txt
```



# HOW TO EDIT FILE LOCALLY:

1. Download the codebase from this repository.
1. make the changes you want to see.
1. Save your changes.
1. Open the 'remakeexecutable.sh' file in an IDE or text editor. and change line 2 to the location of emeraldnotes root directory.
1.  Run the 'remakeexecutable.sh' file in terminal to create a new executable file
1. Run the new executable file to test
1. ENJOY!
