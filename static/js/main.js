document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeToggle) themeToggle.checked = true;
    }

    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            if (themeToggle.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    const previewBtn = document.getElementById('preview-btn');
    const saveBtn = document.getElementById('save-btn');
    const editorArea = document.getElementById('editor-textarea');
    const previewArea = document.getElementById('preview-container');
    const filenameInput = document.getElementById('current-filename');

    function togglePreview() {
        if (!editorArea || !previewArea) return;

        if (editorArea.style.display === 'none') {
            editorArea.style.display = 'block';
            previewArea.style.display = 'none';
            if (previewBtn) previewBtn.textContent = 'Preview';
        } else {
            fetch('/api/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: editorArea.value })
            })
            .then(res => res.json())
            .then(data => {
                previewArea.innerHTML = data.html;
                editorArea.style.display = 'none';
                previewArea.style.display = 'block';
                if (previewBtn) previewBtn.textContent = 'Edit';
            })
            .catch(err => console.error('Error parsing text:', err));
        }
    }

    if (previewBtn) {
        previewBtn.addEventListener('click', togglePreview);
    }

    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'v') {
            e.preventDefault();
            togglePreview();
        }
    });

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            let filename = filenameInput.value;

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