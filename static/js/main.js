document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeToggle) themeToggle.checked = true;
    }
    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
        });
    }

    const editorArea = document.getElementById('editor-textarea');
    const previewContainer = document.getElementById('preview-container');
    const previewBtn = document.getElementById('preview-btn');
    const saveBtn = document.getElementById('save-btn');
    const filenameInput = document.getElementById('current-filename');

    let previewVisible = false;

    function wrapWithCommand(command, arg) {
        const start = editorArea.selectionStart;
        const end = editorArea.selectionEnd;
        const selectedText = editorArea.value.substring(start, end);
        const before = editorArea.value.substring(0, start);
        const after = editorArea.value.substring(end);

        let replacement = '';

        // --- Special Case: snippet (triple backticks) ---
        if (command === 'codeblock') {
            const text = selectedText || 'your code here';
            replacement = '```\n' + text + '\n```';
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }
        if (command === 'hr') {
            const prefix = before.endsWith('\n') || before === '' ? '' : '\n';
            replacement = prefix + '*hr\n';
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }

        if (command === 'link') {
            const url = prompt('Enter URL:');
            if (!url) return;
            const text = selectedText || url;
            replacement = `*link(${text})`;
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }

        // --- Special Case: Image type ---
        if (command === 'img') {
            const url = prompt('Enter image URL:');
            if (!url) return;
            replacement = `*img(${url})`;
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }

        if (command === 'clear') {
            const stripped = selectedText.replace(/\*[a-zA-Z0-9_]+\(([^)]*)\)/g, '$1');
            replacement = stripped;
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }

        if (['bullet', 'number', 'task', 'taskdone'].includes(command)) {
            const lines = selectedText.split('\n');
            const wrappedLines = lines.map(line => {
                const trimmed = line.trim();
                if (!trimmed) return line;
                return `*${command}(${trimmed})`;
            });
            replacement = wrappedLines.join('\n');
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }

        if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'quote', 'bold', 'italic', 'strike', 'code'].includes(command)) {
            const text = selectedText || command;
            replacement = `*${command}(${text})`;
            editorArea.value = before + replacement + after;
            const newCursor = start + replacement.length;
            editorArea.selectionStart = editorArea.selectionEnd = newCursor;
            editorArea.focus();
            return;
        }

        const text = selectedText || command;
        replacement = `*${command}(${text})`;
        editorArea.value = before + replacement + after;
        const newCursor = start + replacement.length;
        editorArea.selectionStart = editorArea.selectionEnd = newCursor;
        editorArea.focus();
    }

    const headingSelect = document.getElementById('heading-select');
    headingSelect.addEventListener('change', () => {
        const val = headingSelect.value;
        if (val) {
            wrapWithCommand(val, '');
        }
        headingSelect.value = '';
    });

    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const command = btn.dataset.command;
            if (!command) return;
            wrapWithCommand(command, '');
        });
    });

    function togglePreview() {
        if (previewVisible) {
            editorArea.style.display = 'block';
            previewContainer.style.display = 'none';
            previewBtn.textContent = 'Preview';
            previewVisible = false;
        } else {
            fetch('/api/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: editorArea.value })
            })
            .then(res => res.json())
            .then(data => {
                previewContainer.innerHTML = data.html;
                editorArea.style.display = 'none';
                previewContainer.style.display = 'block';
                previewBtn.textContent = 'Edit';
                previewVisible = true;
            })
            .catch(err => console.error('Error parsing text:', err));
        }
    }

    if (previewBtn) {
        previewBtn.addEventListener('click', togglePreview);
    }

    // Keyboard shortcut: Ctrl+Shift+V
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'v') {
            e.preventDefault();
            togglePreview();
        }
    });

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            let filename = filenameInput.value.trim();
            if (!filename) {
                filename = prompt("Enter a filename for your project:", "note1.md");
                if (!filename) return;
            }

            fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    filename: filename,
                    content: editorArea.value
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    filenameInput.value = data.filename;
                    alert('Saved successfully!');
                } else {
                    alert('Save failed: ' + data.error);
                }
            })
            .catch(err => console.error('Save error:', err));
        });
    }
});