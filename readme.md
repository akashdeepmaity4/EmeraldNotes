<center><h1>Emerald Notes</h1></center>

## About
Emerald Notes is a simple Markdown editor that allows you to create and edit Markdown files.

1. It is completely local, meaning you can access your files at any time
1. It is very lightweight, suitable for mobile devices or low-end computers.
1. Both executable application as well as localhost webapp available.

#### As I myself am a student, I will be using this exact codebase combined with my second repository 'diagramappfornotes' for my personal notetaking in college or just during self-study. I will be keeping this codebase updated and implement new features as I learn more and more throughout my Computer Science journey.

## Features

- Markdown support
- Custom commands
- Dark mode

## Locations of files and how to change them:

- The current path is 'D:/projects/emeraldnotes/' , to change directory path, change download location
- The current path where notes would be saved is '/storage' , to change that, refer to line 26 in '/app/app.py'
<br>
<br>

## How to Use

1. Download the '.exe' from the root directory and run it (totally safe, however personal discretion advised)

<h2>OR</h2>

1. Download the codebase from this repository
1. Run the app.py file using python in terminal
   
```
Your_drive_letter:
cd path/to/your/root/directory
cd app
python app.py
```

- Example-

  ```
  D:
  cd projects/emeraldnotes
  cd app
  python app.py
  ```
  
3. Open your browser and navigate to http://localhost:5000

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

1. Download the codebase from this repository
1. make the changes you want to see
1. Run the app.py file using python in terminal
```
cd path/to/root/directory
cd app
python app.py
```
3. Open your browser and navigate to http://localhost:5000 to test
4. Run the 'remakeexecutable.sh' file in terminal to create a new executable file
5. Run the new executable file to test
6. ENJOY!
