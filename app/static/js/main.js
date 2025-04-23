// Global functions and utilities for the Fantasy Baseball Tracker

// Format a date to a readable string
function formatDate(dateString) {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Format a number with commas
function formatNumber(num) {
    if (num === undefined || num === null) return '0';
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Show a notification
function showNotification(message, type = 'info') {
    const notificationArea = document.getElementById('notification-area');
    
    if (!notificationArea) {
        // Create notification area if it doesn't exist
        const newNotificationArea = document.createElement('div');
        newNotificationArea.id = 'notification-area';
        newNotificationArea.className = 'position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(newNotificationArea);
    }
    
    const id = 'notification-' + Date.now();
    const html = `
        <div id="${id}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${type === 'error' ? 'bg-danger text-white' : ''}">
                <strong class="me-auto">${type === 'error' ? 'Error' : 'Notification'}</strong>
                <small>Just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    document.getElementById('notification-area').innerHTML += html;
    
    const toastEl = document.getElementById(id);
    const toast = new bootstrap.Toast(toastEl, {
        animation: true,
        autohide: true,
        delay: 5000
    });
    toast.show();
    
    // Remove after hiding
    toastEl.addEventListener('hidden.bs.toast', function () {
        toastEl.remove();
    });
}

// Check API status periodically
function checkApiStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            const statusEl = document.getElementById('auth-status');
            if (statusEl) {
                if (data.auth_status) {
                    statusEl.innerHTML = '<span class="badge bg-success">Connected</span>';
                } else {
                    statusEl.innerHTML = '<span class="badge bg-danger">Disconnected</span>';
                }
            }
        })
        .catch(error => {
            console.error('Error checking API status:', error);
        });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Create notification area
    if (!document.getElementById('notification-area')) {
        const notificationArea = document.createElement('div');
        notificationArea.id = 'notification-area';
        notificationArea.className = 'position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(notificationArea);
    }
    
    // Check API status initially and then every 60 seconds
    checkApiStatus();
    setInterval(checkApiStatus, 60000);
});
