import webview
import app.py

if __name__ == '__main__':
    webview.create_window('Emerald Notes', app.py)
    webview.start()