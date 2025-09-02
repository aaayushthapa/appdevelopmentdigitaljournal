// static/js/assignments.js

document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileInput = document.getElementById('submission-file');
    const fileNameDisplay = document.getElementById('file-name-display');
    const selectedFileName = document.getElementById('selected-file-name');
    const removeFileBtn = document.getElementById('remove-file-btn');
    
    if (fileUploadArea && fileInput) {
        // Click on upload area to trigger file input
        fileUploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Drag and drop functionality
        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });
        
        fileUploadArea.addEventListener('dragleave', function() {
            fileUploadArea.classList.remove('dragover');
        });
        
        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileNameDisplay();
            }
        });
        
        // File input change event
        fileInput.addEventListener('change', updateFileNameDisplay);
        
        // Remove file button
        removeFileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            fileInput.value = '';
            fileNameDisplay.style.display = 'none';
            fileUploadArea.style.display = 'block';
        });
    }
    
    function updateFileNameDisplay() {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            selectedFileName.textContent = file.name;
            fileNameDisplay.style.display = 'flex';
            fileUploadArea.style.display = 'none';
        }
    }
    
    // Form validation
    const submitForm = document.getElementById('submit-form');
    if (submitForm) {
        submitForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('submission-file');
            const comments = document.getElementById('comments');
            
            // Check if at least one field is filled
            if (!fileInput.files.length && comments.value.trim() === '') {
                e.preventDefault();
                alert('Please either upload a file or add comments to your submission.');
            }
        });
    }
});