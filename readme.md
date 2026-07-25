# Emerald Notes

## About
Emerald Notes is a simple Markdown editor that allows you to create and edit Markdown files.

1. It is completely local, meaning you can access your files at any time
1. It is very lightweight, suitable for mobile devices or low-end computers.

#### As I myself am a student, I will be using this exact codebase for my personal notetaking in college or just during self-study. I will keep this codebase updated and implement new features as I learn more and more throughout my academic journey.

## Features
- Markdown support
- Custom commands
- Dark mode

## How to Use
1. Download the codebase from this repository
1. Run the app.py file using python in terminal
```
python app.py
```
3. Open your browser and navigate to http://localhost:5000

## Dependencies
- Python 3.x
- Flask
- Jinja2

```
#installing the dependencies at once
pip install -r requirements.txt
```


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

