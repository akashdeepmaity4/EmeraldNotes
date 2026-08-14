import os
import re
import sys
import json
from flask import render_template as r
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, redirect, url_for

'''
KEEP DEBUG FALSE!
'''

# Resource path for PyInstaller
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(base_path) == 'app':
            base_path = os.path.dirname(base_path)
    return os.path.join(base_path, relative_path)

app = Flask(__name__,
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(PROJECT_ROOT, 'config.json')

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default = {"storage_path": os.path.join(PROJECT_ROOT, 'storage')}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default, f, indent=2)
        return default
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config_data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=2)

config = load_config()
STORAGE_PATH = config.get('storage_path', os.path.join(PROJECT_ROOT, 'storage'))

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

# Main functionality
def parse(text):
    return text

def to_markdown(text):
    return text

def get_preview(content, max_chars=140):
    # ... (unchanged)
    snippet_lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r'^#{1,6}\s*', '', stripped)
        stripped = re.sub(r'^[-*]\s+(\[[ xX]\]\s*)?', '', stripped)
        stripped = re.sub(r'^\d+\.\s+', '', stripped)
        stripped = re.sub(r'^>\s*', '', stripped)
        stripped = stripped.strip('`')
        stripped = re.sub(r'\*\*(.*?)\*\*', r'\1', stripped)
        stripped = re.sub(r'\*(.*?)\*', r'\1', stripped)
        stripped = re.sub(r'~~(.*?)~~', r'\1', stripped)
        if stripped.startswith('```') or stripped == '---':
            continue
        snippet_lines.append(stripped)
        if len(' '.join(snippet_lines)) >= max_chars:
            break

    text = ' '.join(snippet_lines).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + '…'
    return text or "(empty note)"

#routing
@app.route('/')
def home():
    filenames = [f for f in os.listdir(STORAGE_PATH) if f.endswith(('.md', '.txt'))]
    if not filenames:
        return r('index.html')

    projects = []
    for fname in filenames:
        filepath = os.path.join(STORAGE_PATH, fname)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            preview = get_preview(content)
        except OSError:
            preview = "(unable to read file)"
        projects.append({'filename': fname, 'preview': preview})

    return r('index.html', projects=projects)

@app.route('/new')
def new_project():
    return r('index.html', filename='', content='')

@app.route('/edit/<filename>')
def edit_project(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(STORAGE_PATH, filename)
    if not filename or os.path.dirname(filepath) != STORAGE_PATH:
        return redirect(url_for('home'))
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return r('index.html', filename=filename, content=content)
    return redirect(url_for('home'))

@app.route('/api/parse', methods=['POST'])
def parse_text():
    data = request.get_json() or {}
    raw_text = data.get('text', '')
    parsed_html = parse(raw_text)
    return jsonify({'html': parsed_html})

@app.route('/api/save', methods=['POST'])
def save_project():
    data = request.get_json() or {}
    filename = data.get('filename')
    content = data.get('content', '')

    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    filename = secure_filename(filename)
    if not filename:
        return jsonify({'error': 'Invalid filename'}), 400

    if not (filename.endswith('.md') or filename.endswith('.txt')):
        filename += '.md'

    filepath = os.path.join(STORAGE_PATH, filename)
    if os.path.dirname(filepath) != STORAGE_PATH:
        return jsonify({'error': 'Invalid filename'}), 400

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(to_markdown(content))
    return jsonify({'success': True, 'filename': filename})

@app.route('/get_storage_path', methods=['GET'])
def get_storage_path():
    return jsonify({'path': STORAGE_PATH})

@app.route('/set_storage_path', methods=['POST'])
def set_storage_path():
    global STORAGE_PATH
    data = request.get_json()
    if not data or 'path' not in data:
        return jsonify({'success': False, 'error': 'Missing path'}), 400

    new_path = data['path'].strip()
    if not new_path:
        return jsonify({'success': False, 'error': 'Path cannot be empty'}), 400

    if not os.path.exists(new_path):
        return jsonify({'success': False, 'error': f'Path "{new_path}" does not exist on server'}), 400
    if not os.access(new_path, os.W_OK):
        return jsonify({'success': False, 'error': f'Path "{new_path}" is not writable'}), 400

    STORAGE_PATH = new_path
    config['storage_path'] = new_path
    save_config(config)

    return jsonify({'success': True, 'path': new_path})

if __name__ == '__main__':
    app.run(debug=False)
