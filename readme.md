<center><h1>Emerald Notes</h1></center>

## About
Emerald Notes is a simple Markdown editor that allows you to create and edit Markdown files.


1. It is completely local, meaning you can access your files at any time
1. It is very lightweight, suitable for mobile devices or low-end computers.
1. Both executable application as well as localhost webapp available.
1. Can be locally run on all major OSs, but .exe application can ONLY be run on windows.

#### I will be using this exact codebase combined with my second repository 'diagramappfornotes' for my personal notetaking in college or just during self-study. I will be keeping this codebase updated and implement new features as I learn more and more throughout my Computer Science journey.

## Features

- Markdown support with GUI formatting toolbar
- .exe app, localhost webapp AND local webapp using Pywebview
- Native Dark mode support throughout


## How to Use

1. Download the codebase, run 'remakeexecutable.sh' via Bash to make a safe application.

<h2>OR</h2>

1. Download the codebase from this repository
1. Run the launcher.py file using python in Command Prompt/ Bourne Again Shell

<h2>OR</h2>

1. Download the codebase, and run 'app.py' using python 
   
```
cd path/to/your/root/directory
cd app
python app.py
```

- Example-

  ```
  C:
  cd emeraldnotes
  cd app
  python app.py
  ```
  
2. Open your browser and navigate to http://localhost:5000

## Dependencies
- Python 3.x
- Flask
- pyinstaller
- pywebview
- Jinja2

### Install Dependencies

```
pip install -r requirements.txt
```

# HOW TO EDIT FILE LOCALLY:

1. Download the codebase from this repository.
1. make the changes you want to see.
1. Save your changes.
4. Run the 'remakeexecutable.sh' file in terminal to create a new executable file
5. Run the new executable file to test
6. ENJOY!
