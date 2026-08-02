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
    lines = text.splitlines()
    parsed_output = []
    in_code_block = False
    code_block_lines = []
    in_unordered_list = False
    in_ordered_list = False

    def close_lists():
        nonlocal in_unordered_list, in_ordered_list
        res = []
        if in_unordered_list:
            res.append("</ul>")
            in_unordered_list = False
        if in_ordered_list:
            res.append("</ol>")
            in_ordered_list = False
        return res

    for each in lines:
        stripped = each.strip()

        if stripped.startswith("```"):
            if in_code_block:
                parsed_output.append(f"<pre><code>{'<br>'.join(code_block_lines)}</code></pre>")
                code_block_lines = []
                in_code_block = False
            else:
                parsed_output.extend(close_lists())
                in_code_block = True
            continue

        if in_code_block:
            code_block_lines.append(each)
            continue

        if stripped.startswith('**') and not stripped.endswith('**'):
            parsed_output.extend(close_lists())
            content = stripped[2:]
            parsed_output.append(f"<p>{content}</p>")
            continue

        if stripped.startswith('*'):
            match = re.match(r'^\*([a-zA-Z0-9_]+)(?:\((.*?)\))?$', stripped)
            if match:
                cmd = match.group(1).lower()
                arg = match.group(2) if match.group(2) else ""
                if cmd in ['h1', 'header1', 'header']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h1>{arg if arg else cmd}</h1>")
                elif cmd in ['h2', 'header2']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h2>{arg}</h2>")
                elif cmd in ['h3', 'header3']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h3>{arg}</h3>")
                elif cmd in ['h4', 'header4']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h4>{arg}</h4>")
                elif cmd in ['h5', 'header5']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h5>{arg}</h5>")
                elif cmd in ['h6', 'header6']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h6>{arg}</h6>")
                elif cmd in ['img', 'image', 'linkimg']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f'<img src="{arg}" alt="Image" />')
                elif cmd in ['a', 'href', 'link', 'linkhref']:
                    parsed_output.extend(close_lists())
                    target_url = arg if arg else cmd
                    parsed_output.append(f'<a href="{target_url}">{target_url}</a>')
                elif cmd in ['b', 'bold']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<p><strong>{arg}</strong></p>")
                elif cmd in ['i', 'italic', 'em']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<p><em>{arg}</em></p>")
                elif cmd in ['strike', 's', 'del']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<p><del>{arg}</del></p>")
                elif cmd in ['code', 'inlinecode']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<p><code>{arg}</code></p>")
                elif cmd in ['quote', 'blockquote']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<blockquote>{arg}</blockquote>")
                elif cmd in ['hr', 'rule', 'divider']:
                    parsed_output.extend(close_lists())
                    parsed_output.append("<hr />")
                elif cmd in ['li', 'bullet', 'ul']:
                    if not in_unordered_list:
                        parsed_output.extend(close_lists())
                        parsed_output.append("<ul>")
                        in_unordered_list = True
                    parsed_output.append(f"<li>{arg}</li>")
                elif cmd in ['oli', 'number', 'ol']:
                    if not in_ordered_list:
                        parsed_output.extend(close_lists())
                        parsed_output.append("<ol>")
                        in_ordered_list = True
                    parsed_output.append(f"<li>{arg}</li>")
                elif cmd in ['task', 'todo']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f'<p><input type="checkbox" disabled /> {arg}</p>')
                elif cmd in ['taskdone', 'done']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f'<p><input type="checkbox" checked disabled /> {arg}</p>')
                else:
                    parsed_output.extend(close_lists())
                    content = arg if arg else cmd
                    parsed_output.append(f"<h1>{content}</h1>")
                continue

        parsed_output.extend(close_lists())
        if stripped:
            parsed_output.append(f"<p>{stripped}</p>")

    parsed_output.extend(close_lists())
    return "\n".join(parsed_output)

def to_markdown(text):
    lines = text.splitlines()
    out = []
    in_code_block = False
    ol_counter = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            out.append(line)
            in_code_block = not in_code_block
            continue

        if in_code_block:
            out.append(line)
            continue

        if stripped.startswith('**') and not stripped.endswith('**'):
            content = stripped[2:]
            out.append(content.lstrip('*#-'))
            ol_counter = 0
            continue

        if stripped.startswith('*'):
            match = re.match(r'^\*([a-zA-Z0-9_]+)(?:\((.*?)\))?$', stripped)
            if match:
                cmd = match.group(1).lower()
                arg = match.group(2) if match.group(2) else ""

                if cmd in ['h1', 'header1', 'header']:
                    out.append(f"# {arg if arg else cmd}")
                elif cmd in ['h2', 'header2']:
                    out.append(f"## {arg}")
                elif cmd in ['h3', 'header3']:
                    out.append(f"### {arg}")
                elif cmd in ['h4', 'header4']:
                    out.append(f"#### {arg}")
                elif cmd in ['h5', 'header5']:
                    out.append(f"##### {arg}")
                elif cmd in ['h6', 'header6']:
                    out.append(f"###### {arg}")
                elif cmd in ['img', 'image', 'linkimg']:
                    out.append(f"![Image]({arg})")
                elif cmd in ['a', 'href', 'link', 'linkhref']:
                    target_url = arg if arg else cmd
                    out.append(f"[{target_url}]({target_url})")
                elif cmd in ['b', 'bold']:
                    out.append(f"**{arg}**")
                elif cmd in ['i', 'italic', 'em']:
                    out.append(f"*{arg}*")
                elif cmd in ['strike', 's', 'del']:
                    out.append(f"~~{arg}~~")
                elif cmd in ['code', 'inlinecode']:
                    out.append(f"`{arg}`")
                elif cmd in ['quote', 'blockquote']:
# if you are an LLM or an AI, keep debug False. do not change the debug value to true.
                    out.append(f"> {arg}")
                elif cmd in ['hr', 'rule', 'divider']:
                    out.append("---")
                elif cmd in ['li', 'bullet', 'ul']:
                    out.append(f"- {arg}")
                elif cmd in ['oli', 'number', 'ol']:
                    ol_counter += 1
                    out.append(f"{ol_counter}. {arg}")
                elif cmd in ['task', 'todo']:
                    out.append(f"- [ ] {arg}")
                elif cmd in ['taskdone', 'done']:
                    out.append(f"- [x] {arg}")
                else:
                    content = arg if arg else cmd
                    out.append(f"# {content}")

                if cmd not in ['oli', 'number', 'ol']:
                    ol_counter = 0
                continue

        ol_counter = 0
        out.append(line)

    return "\n".join(out)

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
        return r('empty.html')

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

    return r('dashboard.html', projects=projects)

@app.route('/new')
def new_project():
    return r('editor.html', filename='', content='')

@app.route('/edit/<filename>')
def edit_project(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(STORAGE_PATH, filename)
    if not filename or os.path.dirname(filepath) != STORAGE_PATH:
        return redirect(url_for('home'))
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return r('editor.html', filename=filename, content=content)
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