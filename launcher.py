import webview
from app.py import app

if __name__ == '__main__':
    webview.create_window('Emerald Notes', app)
    webview.start()