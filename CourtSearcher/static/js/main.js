// Main JavaScript for Court Case Search Application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading state for buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        const form = button.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                if (form.checkValidity()) {
                    button.disabled = true;
                    const originalText = button.innerHTML;
                    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                    
                    // Re-enable button after 30 seconds as fallback
                    setTimeout(function() {
                        button.disabled = false;
                        button.innerHTML = originalText;
                    }, 30000);
                }
            });
        }
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Table row click handling for recent searches
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        const link = row.querySelector('a');
        if (link) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(e) {
                if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                    link.click();
                }
            });
        }
    });

    // Enhanced form input handling
    const numberInputs = document.querySelectorAll('input[type="text"][pattern*="0-9"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            // Allow only numbers
            e.target.value = e.target.value.replace(/[^0-9]/g, '');
        });
        
        input.addEventListener('paste', function(e) {
            // Handle paste events
            setTimeout(function() {
                e.target.value = e.target.value.replace(/[^0-9]/g, '');
            }, 10);
        });
    });

    console.log('Court Case Search Application initialized successfully');
});
