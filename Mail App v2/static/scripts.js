document.addEventListener('DOMContentLoaded', function() {
    const openFormButton = document.getElementById('openFormButton');
    const minimizeFormButton = document.getElementById('minimizeFormButton');
    const emailForm = document.getElementById('form_container');
    const Emailform = document.getElementById('emailForm');
    const emailList = document.getElementById('emailList');
    const emailDetails = document.getElementById('emailDetails');
    const detailTo = document.getElementById('detailTo');
    const detailSubject = document.getElementById('detailSubject');
    const detailMessage = document.getElementById('detailMessage');
    const loader = document.getElementById('loader'); // Loader element

    openFormButton.addEventListener('click', function() {
        emailForm.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Disable scrolling on background
    });

    minimizeFormButton.addEventListener('click', function() {
        emailForm.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling on background
    });

    Emailform.addEventListener('submit', function(event) {
        event.preventDefault();
        resetErrorMessages();

        if (!validateForm()) {
            return;
        }

        const formData = new FormData(Emailform);

        // Show loader before making fetch request
        loader.style.display = 'block';

        fetch('/send_email', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        }).then(data => {
            alert(data);
            location.reload(); // Refresh page after sending email (you may want a better UI update)
        }).catch(error => {
            console.error('Error:', error);
            showErrorMessage('An error occurred while sending the email.');
        }).finally(() => {
            // Hide loader after fetch request completes
            loader.style.display = 'none';
            emailForm.style.display = 'none';
            document.body.style.overflow = 'auto'; // Restore scrolling on background
        });
    });

    emailList.addEventListener('click', function(event) {
        const target = event.target.closest('.email-item');
        if (target) {
            const to = target.getAttribute('data-to');
            const subject = target.getAttribute('data-subject');
            const message = target.getAttribute('data-message');

            detailTo.textContent = to;
            detailSubject.textContent = subject;
            detailMessage.textContent = message;

            emailDetails.classList.add('active');
        }
    });

    function validateForm() {
        let isValid = true;

        // Validate 'To' email
        const toInput = document.getElementById('to');
        if (!isValidEmail(toInput.value.trim())) {
            showErrorMessage('Please enter a valid email address in the "To" field.');
            isValid = false;
        }

        // Validate 'Subject'
        const subjectInput = document.getElementById('subject');
        if (subjectInput.value.trim() === '') {
            showErrorMessage('Please enter a subject.');
            isValid = false;
        }

        // Validate 'Message'
        const messageInput = document.getElementById('message');
        if (messageInput.value.trim() === '') {
            showErrorMessage('Please enter a message.');
            isValid = false;
        }

        return isValid;
    }

    function isValidEmail(email) {
        // Simple email validation regex
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showErrorMessage(message) {
        const errorContainer = document.getElementById('errorContainer');
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = message;
        errorContainer.appendChild(errorMessage);
    }

    function resetErrorMessages() {
        const errorContainer = document.getElementById('errorContainer');
        errorContainer.innerHTML = '';
    }
});
