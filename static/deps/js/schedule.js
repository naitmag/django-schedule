document.addEventListener("DOMContentLoaded", function () {
        const prevWeekButton = document.getElementById("prev-week");
        const nextWeekButton = document.getElementById("next-week");
        const currentWeekButton = document.getElementById("current-week-btn");
        const weekInput = document.getElementById("week-input");
        const submitWeekButton = document.getElementById("submit-week");
        const groupNotification = document.getElementById("group-notification");
        const currentWeekDisplay = document.getElementById("current-week");

        // Изначально задаем номер учебной недели и информацию о группах
        let currentWeek = 1; // начальное значение для текущей недели
        let selectedWeek = 1; // выбранная пользователем неделя (начально совпадает с текущей)

        const userGroup = "Ваша группа"; // Замените на название вашей группы
        const displayedGroup = "Другая группа"; // Замените на группу, для которой показывается расписание

        // Функция для обновления отображаемого номера недели
        function updateWeekDisplay() {
            currentWeekDisplay.textContent = selectedWeek;


            // Обновляем состояние кнопки "Текущая неделя"
            updateCurrentWeekButtonState();
        }

        // Функция для обновления состояния кнопки "Текущая неделя"
        function updateCurrentWeekButtonState() {
            if (selectedWeek === currentWeek) {
                currentWeekButton.classList.add('disabled');
                currentWeekButton.disabled = true; // Кнопка неактивна
            } else {
                currentWeekButton.classList.remove('disabled');
                currentWeekButton.disabled = false; // Кнопка активна
            }
        }

        // Обработчики событий для кнопок
        prevWeekButton.addEventListener("click", function () {
            if (selectedWeek > 1) {
                selectedWeek--;
                updateWeekDisplay();
            }
        });

        nextWeekButton.addEventListener("click", function () {
            selectedWeek++;
            updateWeekDisplay();
        });

        currentWeekButton.addEventListener("click", function () {
            if (selectedWeek !== currentWeek) {
                selectedWeek = currentWeek; // возвращаемся к текущей неделе
                updateWeekDisplay();
            }
        });

        submitWeekButton.addEventListener("click", function () {
            const inputWeek = parseInt(weekInput.value, 10);
            if (inputWeek > 0) {
                selectedWeek = inputWeek;
                updateWeekDisplay();
            }
        });

        // Инициализация отображения при загрузке страницы
        updateWeekDisplay();
    });