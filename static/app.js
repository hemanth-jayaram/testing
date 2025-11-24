// Main JavaScript for FL Phishing Detection App

// Global variables
let trainingActive = false;
let accuracyChart = null;

// Initialize when document is ready
$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-refresh stats on home page
    if (window.location.pathname === '/') {
        setInterval(refreshStats, 30000); // Refresh every 30 seconds
    }
});

// Refresh dashboard statistics
function refreshStats() {
    $.get('/api/stats')
        .done(function(data) {
            $('#dataset-count').text(data.dataset_count);
            $('#model-count').text(data.model_count);
            $('#latest-accuracy').text((data.latest_accuracy * 100).toFixed(2) + '%');
        })
        .fail(function() {
            console.log('Failed to refresh stats');
        });
}

// File upload validation
function validateFile(input) {
    const file = input.files[0];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (file) {
        if (!file.name.toLowerCase().endsWith('.csv')) {
            alert('Please select a CSV file');
            input.value = '';
            return false;
        }
        
        if (file.size > maxSize) {
            alert('File size must be less than 16MB');
            input.value = '';
            return false;
        }
    }
    
    return true;
}

// Show loading spinner
function showLoading(element) {
    const spinner = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>';
    element.html(spinner + element.text()).prop('disabled', true);
}

// Hide loading spinner
function hideLoading(element, originalText) {
    element.html(originalText).prop('disabled', false);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success message
        const toast = new bootstrap.Toast(document.getElementById('copyToast'));
        toast.show();
    });
}

// Smooth scroll to element
function scrollToElement(elementId) {
    document.getElementById(elementId).scrollIntoView({
        behavior: 'smooth'
    });
}

// Debounce function for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global use
window.validateFile = validateFile;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.formatFileSize = formatFileSize;
window.formatDate = formatDate;
window.copyToClipboard = copyToClipboard;
window.scrollToElement = scrollToElement;