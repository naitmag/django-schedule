//document.getElementById('phone').addEventListener('input', function (e) {
//    var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,2})(\d{0,3})(\d{0,4})/);
//    e.target.value = !x[2] ? x[1] : '+375 (' + x[2] + ') ' + x[3] + (x[4] ? '-' + x[4].slice(0, 2) : '');
//});

    const form = document.getElementById('register-form');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    const registerButton = document.getElementById('register-button');
    const dataAgreement = document.getElementById('data-agreement');
    const errorMessage = document.getElementById('error-message');
    const validationMessage = document.getElementById('validation-message');

    function validateForm() {
        const allFieldsFilled = form.checkValidity();
        const passwordsMatch = password.value === confirmPassword.value;
        const groupSelected = document.getElementById('group').value !== "";

        let message = "";

        if (!allFieldsFilled) {
            message = "Все обязательные поля должны быть заполнены.";
        } else if (!passwordsMatch) {
            message = "Пароли не совпадают.";
        } else if (!dataAgreement.checked) {
            message = "Вы должны согласиться с обработкой персональных данных.";
        }

        if (message) {
            validationMessage.style.display = 'block';
            validationMessage.textContent = message;
        } else {
            validationMessage.style.display = 'none';
        }

        if (allFieldsFilled && passwordsMatch && dataAgreement.checked && groupSelected) {
            registerButton.classList.add('active');
            registerButton.disabled = false;
            errorMessage.style.display = 'none';
        } else {
            registerButton.classList.remove('active');
            registerButton.disabled = true;
            if (!passwordsMatch && confirmPassword.value !== "") {
                errorMessage.style.display = 'block';
            } else {
                errorMessage.style.display = 'none'; } } }

            // События для проверки валидации формы
            form.addEventListener('input', validateForm);
            confirmPassword.addEventListener('input', validateForm);
            dataAgreement.addEventListener('change', validateForm);
            document.getElementById('group').addEventListener('change', validateForm);
