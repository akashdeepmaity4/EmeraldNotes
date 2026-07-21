import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def parse_custom_markdown(text):
    lines = text.splitlines()
    parsed_output = []

    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('**'):
            content = stripped[2:]
            parsed_output.append(f"<p>{content}</p>")
            continue

        if stripped.startswith('*'):
            match = re.match(r'^\*([a-zA-Z0-9]+)(?:\((.*?)\))?$', stripped)
            
            if match:
                cmd = match.group(1).lower()
                arg = match.group(2) if match.group(2) else ""

                if cmd == 'header1':
                    parsed_output.append(f"<h1>{arg}</h1>")
                elif cmd == 'header2':
                    parsed_output.append(f"<h2>{arg}</h2>")
                elif cmd == 'linkimg':
                    parsed_output.append(f'<img src="{arg}" alt="Image" />')
                elif cmd == 'linkhref':
                    parsed_output.append(f'<a href="{arg}">{arg}</a>')
                else:
                    if arg:
                        parsed_output.append(f"<h1>{arg}</h1>")
                    else:
                        parsed_output.append(f"<h1>{cmd}</h1>")
            else:
                parsed_output.append(f"<p>{stripped[1:]}</p>")
            continue

        if stripped:
            parsed_output.append(f"<p>{stripped}</p>")

    return "\n".join(parsed_output)


@app.route('/')
def home():
    files = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.txt')]
    
    if not files:
        return render_template('empty.html')
    
    return render_template('dashboard.html', projects=files)


@app.route('/new')
def new_project():
    return render_template('editor.html', filename='', content='')


@app.route('/edit/<filename>')
def edit_project(filename):
    filepath = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return render_template('editor.html', filename=filename, content=content)
    return redirect(url_for('home'))


@app.route('/api/parse', methods=['POST'])
def parse_text():
    data = request.get_json() or {}
    raw_text = data.get('text', '')
    parsed_html = parse_custom_markdown(raw_text)
    return jsonify({'html': parsed_html})


@app.route('/api/save', methods=['POST'])
def save_project():
    data = request.get_json() or {}
    filename = data.get('filename')
    content = data.get('content', '')

    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    if not filename.endswith('.txt'):
        filename += '.txt'

    filepath = os.path.join(STORAGE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return jsonify({'success': True, 'filename': filename})


if __name__ == '__main__':
    app.run(debug=True)