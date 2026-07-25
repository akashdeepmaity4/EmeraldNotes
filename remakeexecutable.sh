cd D:\projects\emeraldnotes
rmdir /s build
rmdir /s dist
del *.spec
pyinstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "app;app" --add-data "storage;storage" --hidden-import flask --hidden-import jinja2 --hidden-import app --hidden-import app.app --paths . launcher.py