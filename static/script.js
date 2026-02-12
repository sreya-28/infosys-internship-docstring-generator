let currentFileName = '';

function triggerFile() {
    document.getElementById('fileInput').click();
}

document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const fileInfo = document.getElementById('fileInfo');
    
    if (file) {
        currentFileName = file.name;
        fileInfo.textContent = `✅ ${file.name}`;
        document.getElementById('codeInput').value = '';
    } else {
        currentFileName = '';
        fileInfo.textContent = 'No file selected';
    }
});

async function generateAST() {
    const fileInput = document.getElementById('fileInput');
    const codeInput = document.getElementById('codeInput').value;
    const resultArea = document.getElementById('resultArea');
    const outputSection = document.getElementById('outputSection');
    
    // Validation
    if (!fileInput.files[0] && !codeInput.trim()) {
        alert('Please upload a file OR paste code!');
        return;
    }
    
    // Show loading
    resultArea.textContent = '🔄 Generating AST...';
    outputSection.style.display = 'block';
    
    const formData = new FormData();
    
    if (fileInput.files[0]) {
        formData.append('file', fileInput.files[0]);
    } else {
        formData.append('code_input', codeInput);
    }
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultArea.textContent = data.ast;
        } else {
            resultArea.textContent = data.error;
            resultArea.style.color = '#ff6b6b';
        }
    } catch (error) {
        resultArea.textContent = `❌ Network error: ${error.message}`;
    }
}

function copyAST() {
    const resultArea = document.getElementById('resultArea');
    navigator.clipboard.writeText(resultArea.textContent).then(() => {
        const btn = event.target;
        const original = btn.textContent;
        btn.textContent = '✅ Copied!';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.textContent = original;
            btn.style.background = '';
        }, 2000);
    });
}
