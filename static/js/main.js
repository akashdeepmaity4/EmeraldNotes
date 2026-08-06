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
    if (editorArea) {
        const previewContainer = document.getElementById('preview-container');
        const previewBtn = document.getElementById('preview-btn');
        const saveBtn = document.getElementById('save-btn');
        const filenameInput = document.getElementById('current-filename');
        const headingSelect = document.getElementById('heading-select');

        let previewVisible = false;
        let hasUnsavedChanges = false;
        let lastAutosaveLineCount = editorArea.value.split('\n').length;
        let autosaveInProgress = false;

        function saveDocument({ saveAs = false, silent = false } = {}) {
            let filename = filenameInput.value.trim();
            if (saveAs || !filename) {
                filename = prompt(
                    'Enter a filename for your project:',
                    saveAs ? (filename || 'note1.txt') : 'note1.txt'
                );
                if (!filename) return Promise.resolve(false);
            }

            return fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    filename: filename,
                    content: editorArea.value
                })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) {
                    if (!silent) alert('Save failed: ' + data.error);
                    return false;
                }

                filenameInput.value = data.filename;
                hasUnsavedChanges = false;
                lastAutosaveLineCount = editorArea.value.split('\n').length;
                if (!silent) alert('Saved successfully!');
                return true;
            })
            .catch(err => {
                console.error('Save error:', err);
                if (!silent) alert('Could not save the file. See console.');
                return false;
            });
        }

        function createNewDocument() {
            const newPageUrl = document.querySelector('.toolbar-left a.pill-btn')?.href || '/new';
            if (!hasUnsavedChanges || !editorArea.value.trim()) {
                window.location.href = newPageUrl;
                return;
            }

            saveDocument().then(saved => {
                if (saved) window.location.href = newPageUrl;
            });
        }

        function updatePreview() {
            fetch('/api/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: editorArea.value })
            })
            .then(res => res.json())
            .then(data => {
                previewContainer.innerHTML = data.html;
            })
            .catch(err => console.error('Error parsing text:', err));
        }

        function wrapWithCommand(command, arg) {
            const start = editorArea.selectionStart;
            const end = editorArea.selectionEnd;
            const selectedText = editorArea.value.substring(start, end);
            const before = editorArea.value.substring(0, start);
            const after = editorArea.value.substring(end);

            let replacement = '';
            const applyReplacement = (cursorStart = start + replacement.length, cursorEnd = cursorStart) => {
                editorArea.value = before + replacement + after;
                editorArea.selectionStart = cursorStart;
                editorArea.selectionEnd = cursorEnd;
                editorArea.focus();
                updatePreview();
            };

            if (command === 'codeblock') {
                const text = selectedText;
                replacement = '```\n' + text + '\n```';
                const newCursor = selectedText ? start + replacement.length : start + 4;
                applyReplacement(newCursor);
                return;
            }
            if (command === 'hr') {
                const prefix = before.endsWith('\n') || before === '' ? '' : '\n';
                replacement = prefix + '---\n';
                applyReplacement();
                return;
            }
            if (command === 'clear') {
                const stripped = selectedText;
                replacement = stripped;
                applyReplacement();
                return;
            }
            if (['bullet', 'number', 'task', 'taskdone'].includes(command)) {
                const lineStart = editorArea.value.lastIndexOf('\n', start - 1) + 1;
                const prefix = command === 'bullet' ? '- ' : command === 'number' ? '1. ' : command === 'task' ? '- [ ] ' : '- [x] ';
                replacement = prefix;
                editorArea.value = editorArea.value.substring(0, lineStart) + replacement + editorArea.value.substring(lineStart);
                editorArea.selectionStart = start + replacement.length;
                editorArea.selectionEnd = end + replacement.length;
                editorArea.focus();
                updatePreview();
                return;
            }
            if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'quote', 'bold', 'italic', 'strike', 'code'].includes(command)) {
                const text = selectedText;
                if (command.startsWith('h')) {
                    const lineStart = editorArea.value.lastIndexOf('\n', start - 1) + 1;
                    replacement = `${'#'.repeat(Number(command[1]))} `;
                    editorArea.value = editorArea.value.substring(0, lineStart) + replacement + editorArea.value.substring(lineStart);
                    editorArea.selectionStart = start + replacement.length;
                    editorArea.selectionEnd = end + replacement.length;
                    editorArea.focus();
                    updatePreview();
                    return;
                }
                if (command === 'quote') replacement = `> ${text}`;
                else if (command === 'bold') replacement = `**${text}**`;
                else if (command === 'italic') replacement = `*${text}*`;
                else if (command === 'strike') replacement = `~~${text}~~`;
                else replacement = `\`${text}\``;
                const newCursor = !selectedText && command === 'bold' ? start + 2 : !selectedText && command === 'italic' ? start + 1 : start + replacement.length;
                applyReplacement(newCursor);
                return;
            }

            const text = selectedText || command;
            replacement = text;
            applyReplacement();
        }

        if (headingSelect) {
            headingSelect.addEventListener('change', () => {
                const val = headingSelect.value;
                if (val) {
                    wrapWithCommand(val, '');
                }
                headingSelect.value = '';
            });
        }

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

        editorArea.addEventListener('input', () => {
            hasUnsavedChanges = true;
            const currentLineCount = editorArea.value.split('\n').length;
            if (
                filenameInput.value.trim() &&
                !autosaveInProgress &&
                currentLineCount - lastAutosaveLineCount >= 20
            ) {
                autosaveInProgress = true;
                saveDocument({ silent: true }).finally(() => {
                    autosaveInProgress = false;
                });
            }
        });

        document.addEventListener('keydown', (e) => {
            if (!e.ctrlKey) return;

            if (e.key.toLowerCase() === 'n') {
                e.preventDefault();
                createNewDocument();
                return;
            }

            if (e.key.toLowerCase() === 's') {
                e.preventDefault();
                saveDocument({ saveAs: e.shiftKey });
                return;
            }

            if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'v') {
                e.preventDefault();
                togglePreview();
            }
        });

        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                saveDocument();
            });
        }
    } 


    
    const profileLogo = document.getElementById('profileLogo');
    const modal = document.getElementById('pathModal');
    const cancelBtn = document.getElementById('cancelPathBtn');
    const savePathBtn = document.getElementById('savePathBtn');
    const pathInput = document.getElementById('storagePathInput');
    const currentPathDisplay = document.getElementById('currentPathDisplay');

    function openPathModal() {
        if (!modal) return;

        fetch('/get_storage_path')
            .then(res => res.json())
            .then(data => {
                currentPathDisplay.textContent = data.path;
                pathInput.value = data.path;
                modal.style.display = 'flex';
            })
            .catch(err => {
                console.error('Failed to load path:', err);
                alert('Could not load current storage path.');
            });
    }

    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key.toLowerCase() === 'p') {
            e.preventDefault();
            openPathModal();
        }
    });

    if (profileLogo && modal) {
        profileLogo.addEventListener('click', openPathModal);

        if (cancelBtn) {
            cancelBtn.addEventListener('click', function() {
                modal.style.display = 'none';
            });
        }

        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        if (savePathBtn) {
            savePathBtn.addEventListener('click', function() {
                const newPath = pathInput.value.trim();
                if (!newPath) {
                    alert('Please enter a valid folder path.');
                    return;
                }

                fetch('/set_storage_path', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: newPath })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert('Storage path updated successfully!');
                        currentPathDisplay.textContent = newPath;
                        modal.style.display = 'none';
                        window.location.reload();
                    } else {
                        alert('Error: ' + data.error);
                    }
                })
                .catch(err => {
                    console.error('Failed to save path:', err);
                    alert('Could not save path. See console.');
                });
            });
        }
    }
});
