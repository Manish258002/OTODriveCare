// OTO DriveCare - Main JS

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });

    // Tooltip init
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // Active nav link highlight
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active', 'text-warning');
        }
    });

});

// Geolocation utility
function getUserLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            pos => callback(pos.coords.latitude, pos.coords.longitude),
            err => console.warn('Geolocation error:', err.message)
        );
    } else {
        console.warn('Geolocation not supported');
    }
}
