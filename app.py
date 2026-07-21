import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
STORAGE_DIR = os.path.join(os.path.dirname(__file__), 'storage')

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for

def parse_custom_markdown(text):
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

    for line in lines:
        stripped = line.strip()

        # Handle ``` code blocks
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
            code_block_lines.append(line)
            continue

        # Rule: **word -> treated as plain normal paragraph text (per initial rules)
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

                if cmd in ['h1', 'header1']:
                    parsed_output.extend(close_lists())
                    parsed_output.append(f"<h1>{arg}</h1>")
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
                    parsed_output.append(f'<a href="{arg}">{arg}</a>')
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

                # Lists
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