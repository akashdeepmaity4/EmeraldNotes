# DISCLAIMER
cd D:\projects
# Change this above location to the location you want your codebade to live


cd emeraldnotes
pyinstaller --onefile --windowed --add-data "templates;templates" --add-data "static;static" --add-data "app;app" --add-data "storage;storage" --hidden-import flask --hidden-import jinja2 --hidden-import app --hidden-import app.app --paths . launcher.py
echo Download complete! Removing duplicacies... 

mv dist/launcher.exe launcher.exe
mv launcher.exe EmeraldNotes.exe
rm -rf dist
rm -rf build
rm -f *.spec
echo build complete!