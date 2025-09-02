// static/js/project.js

document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality for log entries
    const logFileUploadArea = document.getElementById('log-file-upload-area');
    const logFileInput = document.getElementById('media');
    const logFileNameDisplay = document.getElementById('log-file-name-display');
    const logSelectedFileName = document.getElementById('log-selected-file-name');
    const logRemoveFileBtn = document.getElementById('log-remove-file-btn');
    
    if (logFileUploadArea && logFileInput) {
        // Click on upload area to trigger file input
        logFileUploadArea.addEventListener('click', function() {
            logFileInput.click();
        });
        
        // Drag and drop functionality
        logFileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            logFileUploadArea.classList.add('dragover');
        });
        
        logFileUploadArea.addEventListener('dragleave', function() {
            logFileUploadArea.classList.remove('dragover');
        });
        
        logFileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            logFileUploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                logFileInput.files = e.dataTransfer.files;
                updateLogFileNameDisplay();
            }
        });
        
        // File input change event
        logFileInput.addEventListener('change', updateLogFileNameDisplay);
        
        // Remove file button
        logRemoveFileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            logFileInput.value = '';
            logFileNameDisplay.style.display = 'none';
            logFileUploadArea.style.display = 'block';
        });
    }
    
    function updateLogFileNameDisplay() {
        if (logFileInput.files.length > 0) {
            const file = logFileInput.files[0];
            logSelectedFileName.textContent = file.name;
            logFileNameDisplay.style.display = 'flex';
            logFileUploadArea.style.display = 'none';
        }
    }
    
    // Form validation
    const logForm = document.getElementById('log-form');
    if (logForm) {
        logForm.addEventListener('submit', function(e) {
            const titleInput = document.getElementById('log-title');
            const contentInput = document.getElementById('log-content');
            
            // Basic validation
            if (titleInput.value.trim() === '') {
                e.preventDefault();
                alert('Please enter a title for your log entry.');
                titleInput.focus();
                return;
            }
            
            if (contentInput.value.trim() === '') {
                e.preventDefault();
                alert('Please enter content for your log entry.');
                contentInput.focus();
                return;
            }
        });
    }
});