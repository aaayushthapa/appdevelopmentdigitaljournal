// static/js/settings.js

document.addEventListener('DOMContentLoaded', function() {
    // Avatar upload functionality
    const avatarUploadArea = document.getElementById('avatar-upload-area');
    const avatarInput = document.getElementById('avatar');
    const avatarFileNameDisplay = document.getElementById('avatar-file-name-display');
    const avatarSelectedFileName = document.getElementById('avatar-selected-file-name');
    const avatarRemoveFileBtn = document.getElementById('avatar-remove-file-btn');
    
    if (avatarUploadArea && avatarInput) {
        // Click on upload area to trigger file input
        avatarUploadArea.addEventListener('click', function() {
            avatarInput.click();
        });
        
        // File input change event
        avatarInput.addEventListener('change', updateAvatarFileNameDisplay);
        
        // Remove file button
        avatarRemoveFileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            avatarInput.value = '';
            avatarFileNameDisplay.style.display = 'none';
            avatarUploadArea.style.display = 'block';
        });
    }
    
    function updateAvatarFileNameDisplay() {
        if (avatarInput.files.length > 0) {
            const file = avatarInput.files[0];
            avatarSelectedFileName.textContent = file.name;
            avatarFileNameDisplay.style.display = 'flex';
            avatarUploadArea.style.display = 'none';
        }
    }
});