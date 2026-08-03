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


# HOW TO USE: (syntax)
@@@
Here is the exact syntax for every command built into your custom parser script:

### **1. Headers**

* **Syntax:** `*h1(Your Header Text)`
* **Aliases:** `*header1`, `*h2` through `*h6`, `*header2` through `*header6`

### **2. Links & Images**

* **Links Syntax:** `*link([https://example.com](https://example.com))`
* *Aliases:* `*a`, `*href`, `*linkhref`


* **Images Syntax:** `*img([https://example.com/image.jpg](https://example.com/image.jpg))`
* *Aliases:* `*image`, `*linkimg`



### **3. Text Formatting**

* **Bold:** `*bold(some text)` *(Alias: `*b`)*
* **Italic:** `*italic(some text)` *(Aliases: `*i`, `*em`)*
* **Strikethrough:** `*strike(some text)` *(Aliases: `*s`, `*del`)*
* **Inline Code:** `*code(print("hello"))` *(Alias: `*inlinecode`)*

### **4. Lists & Tasks**

* **Bullet List Item:** `*bullet(list item text)` *(Aliases: `*li`, `*ul`)*
* **Numbered List Item:** `*number(list item text)` *(Aliases: `*oli`, `*ol`)*
* **Unchecked Task:** `*task(buy groceries)` *(Alias: `*todo`)*
* **Checked Task:** `*taskdone(finish homework)` *(Alias: `*done`)*

### **5. Blockquotes & Dividers**

* **Blockquote:** `*quote(wisdom text here)` *(Alias: `*blockquote`)*
* **Horizontal Divider:** `*hr` *(Aliases: `*rule`, `*divider`)*

### **6. Multiline Code Blocks**

* **Syntax:** Wrap code lines inside triple backticks:
def hello():
print("world")
### **7. Escaping Commands (Plain Text)**

* **Syntax:** `**text here`
* **Behavior:** Forces lines starting with `*` to be treated as a standard, literal paragraph instead of triggering a command.

