// DOM Elements
const authPage = document.getElementById('auth-page');
const dashboardPage = document.getElementById('dashboard-page');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const showSignupBtn = document.getElementById('show-signup');
const logoutBtn = document.getElementById('logout-btn');
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

// Tab Switching
if (tabs.length > 0) {
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
}

// File Upload Functionality
const fileUploads = document.querySelectorAll('.file-upload');
fileUploads.forEach(upload => {
    upload.addEventListener('click', () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.click();
        
        input.addEventListener('change', () => {
            if (input.files.length > 0) {
                upload.innerHTML = `<p>Selected: ${input.files[0].name}</p>`;
            }
        });
    });
});

// Form Validation
if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            alert('Passwords do not match!');
        }
    });
}

// Initialize any dashboard-specific functionality
function initDashboard() {
    // Add any dashboard initialization code here
    console.log('Dashboard initialized');
}

// Check if we're on the dashboard and initialize
if (document.querySelector('.dashboard')) {
    initDashboard();
}
// Function to update assignment counts
function updateAssignmentCounts() {
    fetch('/api/assignment_counts')
        .then(response => response.json())
        .then(data => {
            // Update UI with assignment counts
            document.querySelectorAll('.assignment-count').forEach(element => {
                const assignmentId = element.getAttribute('data-assignment-id');
                if (data[assignmentId]) {
                    element.textContent = `Submissions: ${data[assignmentId]}`;
                }
            });
        })
        .catch(error => console.error('Error fetching assignment counts:', error));
}

// Initialize assignment counts when page loads
if (document.querySelector('.assignment-count')) {
    updateAssignmentCounts();
    // Update every 30 seconds
    setInterval(updateAssignmentCounts, 30000);
}