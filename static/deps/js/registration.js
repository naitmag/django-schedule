
    const form = document.getElementById('register-form');
    const registerButton = document.getElementById('register-button');
    const dataAgreement = document.getElementById('data-agreement');
    const errorMessage = document.getElementById('error-message');
    const validationMessage = document.getElementById('validation-message');

    function validateForm() {
        const allFieldsFilled = form.checkValidity();
        const groupSelected = document.getElementById('group').value !== "";

        let message = "";

        if (!allFieldsFilled) {
            message = "Все обязательные поля должны быть заполнены.";
        }

        if (message) {
            validationMessage.style.display = 'block';
            validationMessage.textContent = message;
        } else {
            validationMessage.style.display = 'none';
        }

        if (allFieldsFilled && groupSelected) {
            registerButton.classList.add('active');
            registerButton.disabled = false;
        } else {
            registerButton.classList.remove('active');
            registerButton.disabled = true;
            }
        }

            // События для проверки валидации формы
            form.addEventListener('input', validateForm);
            document.getElementById('group').addEventListener('change', validateForm);
