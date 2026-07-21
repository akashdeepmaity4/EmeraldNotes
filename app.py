import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')

# Ensure storage directory exists
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def parse_custom_markdown(text):
    """
    Custom parsing rules:
    - **word -> normal paragraph text
    - *word(arg) -> dynamic tags (*header1, *header2, *linkimg, *linkhref, etc.)
    - *word -> default h1 or href based on context/command
    """
    lines = text.splitlines()
    parsed_output = []

    for line in lines:
        stripped = line.strip()
        
        # Rule: **word -> treated as plain normal paragraph text
        if stripped.startswith('**'):
            content = stripped[2:]
            parsed_output.append(f"<p>{content}</p>")
            continue

        # Rule: *word(arg) or *word
        if stripped.startswith('*'):
            # Match command and optional parenthesized argument: *command or *command(arg)
            match = re.match(r'^\*([a-zA-Z0-9]+)(?:\((.*?)\))?$', stripped)
            
            if match:
                cmd = match.group(1).lower()
                arg = match.group(2) if match.group(2) else ""

                # Explicit commands
                if cmd == 'header1':
                    parsed_output.append(f"<h1>{arg}</h1>")
                elif cmd == 'header2':
                    parsed_output.append(f"<h2>{arg}</h2>")
                elif cmd == 'linkimg':
                    parsed_output.append(f'<img src="{arg}" alt="Image" />')
                elif cmd == 'linkhref':
                    parsed_output.append(f'<a href="{arg}">{arg}</a>')
                else:
                    # Default handling if unspecified *word: header or link
                    if arg:
                        parsed_output.append(f"<h1>{arg}</h1>")
                    else:
                        parsed_output.append(f"<h1>{cmd}</h1>")
            else:
                # Fallback for inline or non-matching star syntax
                parsed_output.append(f"<p>{stripped[1:]}</p>")
            continue

        # Plain text
        if stripped:
            parsed_output.append(f"<p>{stripped}</p>")

    return "\n".join(parsed_output)


@app.route('/')
def home():
    # Fetch list of existing projects in storage
    files = [f for f in os.listdir(STORAGE_DIR) if f.endswith('.txt')]
    
    # Page 1: Entry page when no projects are created
    if not files:
        return render_template('empty.html')
    
    # Page 2: Entry page when projects exist
    return render_template('dashboard.html', projects=files)


@app.route('/new')
def new_project():
    # Page 3: Appears when clicking 'new'
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
    # Live preview parsing engine endpoint
    data = request.get_json() or {}
    raw_text = data.get('text', '')
    parsed_html = parse_custom_markdown(raw_text)
    return jsonify({'html': parsed_html})


@app.route('/api/save', methods=['POST'])
def save_project():
    # Endpoint to write files to local storage
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