document.addEventListener('DOMContentLoaded', function () {
    const scheduleContainer = document.querySelector('.schedule-container');
    const currentWeekSpan = document.getElementById('current-week');
    const prevWeekBtn = document.getElementById('prev-week');
    const nextWeekBtn = document.getElementById('next-week');
    const currentWeekBtn = document.getElementById('current-week-btn');
    const goToWeekBtn = document.getElementById('go-week');
    const weekInput = document.getElementById('week-input');

    const queryString = window.location.search
    const urlParams = new URLSearchParams(queryString);

    const group = urlParams.get('group');
    const teacher = urlParams.get('teacher');


    let currentWeek; // Переменная для хранения текущей недели
    let displayedWeek; // Переменная для хранения отображаемой недели

    // Функция для получения расписания и текущей недели
    // Функция для получения расписания и текущей недели
function fetchSchedule() {
    // Формируем базовый URL
    let url = '/schedule/get_schedule/';

    // Проверяем параметры group и teacher, добавляем их в запрос, если они существуют
    const params = [];
    if (group) {
        params.push(`group=${encodeURIComponent(group)}`);
    }
    if (teacher) {
        params.push(`teacher=${encodeURIComponent(teacher)}`);
    }

    // Добавляем параметры к URL, если они есть
    if (params.length > 0) {
        url += '?' + params.join('&');
    }

    // Выполняем запрос
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка при получении расписания');
            }
            return response.json();
        })
        .then(data => {
            // Установка текущей недели
            currentWeek = data.current_week;
            currentWeekSpan.textContent = currentWeek;

            // Отрисовка расписания
            renderSchedule(data.schedule);
            displayedWeek = currentWeek; // Устанавливаем отображаемую неделю
            updateCurrentWeekButton(); // Обновляем кнопку текущей недели
        })
        .catch(error => console.error('Ошибка при получении данных:', error));
}


    // Функция для отрисовки расписания
    function renderSchedule(schedule) {
        scheduleContainer.innerHTML = '';  // Очистка предыдущего расписания

        schedule.forEach(day => {
            // Создаем карточку для каждого дня
            const dayCard = document.createElement('div');
            dayCard.classList.add('schedule-card');

            // Заголовок с названием дня
            const cardHeader = document.createElement('div');
            cardHeader.classList.add('card-header');
            switch (day.title) {
                case 'Понедельник':
                    cardHeader.classList.add('monday');
                    break;
                case 'Вторник':
                    cardHeader.classList.add('tuesday');
                    break;
                case 'Среда':
                    cardHeader.classList.add('wednesday');
                    break;
                case 'Четверг':
                    cardHeader.classList.add('thursday');
                    break;
                case 'Пятница':
                    cardHeader.classList.add('friday');
                    break;
                case 'Суббота':
                    cardHeader.classList.add('saturday');
                    break;
                case 'Воскресенье':
                    cardHeader.classList.add('sunday');
                    break;
            }
            cardHeader.textContent = `${day.title} (${day.date})`; // Присваиваем название дня и дату
            dayCard.appendChild(cardHeader);

            // Тело карточки с занятиями
            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body');

            if (day.lessons.length === 0) {
                cardBody.classList.add('empty');
                const noLessonsText = document.createElement('p');
                noLessonsText.classList.add('no-lesson-title');
                noLessonsText.textContent = 'Занятий нет';
                cardBody.appendChild(noLessonsText);
                const noLessonsDescription = document.createElement('p');
                noLessonsDescription.classList.add('no-lesson-description');
                noLessonsDescription.textContent = 'Отдохните и подготовьтесь к следующему дню.';
                cardBody.appendChild(noLessonsDescription);
            } else {
                day.lessons.forEach(lesson => {
                    const lessonDiv = document.createElement('div');
                    lessonDiv.classList.add('lesson');

                    const lessonTime = document.createElement('div');
                    lessonTime.classList.add('lesson-time');
                    lessonTime.textContent = lesson.timeSlot;
                    lessonDiv.appendChild(lessonTime);

                    const lessonType = document.createElement('div');
                    lessonType.classList.add('lesson-type');
                    lessonType.textContent = lesson.lesson_type;
                    lessonDiv.appendChild(lessonType);

                    const lessonName = document.createElement('a');
                    lessonName.classList.add('lesson-name');
                    lessonName.href = `lesson/${lesson.id}`;
                    lessonName.textContent = lesson.title;
                    lessonDiv.appendChild(lessonName);

                    // Добавление информации о подгруппе
                    if (lesson.subgroup) {
                        const subgroupInfo = document.createElement('div');
                        subgroupInfo.classList.add('subgroup-info');
                        subgroupInfo.textContent = `${lesson.subgroup}`;
                        lessonDiv.appendChild(subgroupInfo);
                    }

                    // Добавление информации о преподавателе
                    const teacherInfo = document.createElement('div');
                    teacherInfo.classList.add('teacher-info');
                    teacherInfo.textContent = `${lesson.teacher}`;
                    lessonDiv.appendChild(teacherInfo);

                    cardBody.appendChild(lessonDiv);
                });
            }

            dayCard.appendChild(cardBody);
            // Добавляем карточку на страницу
            scheduleContainer.appendChild(dayCard);
        });
    }

    // Функция для обновления расписания с выбранной неделей
    // Функция для обновления расписания с выбранной неделей
function updateSchedule(newWeek) {
    if (newWeek < 1 || newWeek > 20) return; // Проверка на диапазон

    // Формируем базовый URL
    let url = `/schedule/get_schedule/?week=${newWeek}`;

    // Проверяем параметры group и teacher, добавляем их в запрос, если они существуют
    const params = [];
    if (group) {
        params.push(`group=${encodeURIComponent(group)}`);
    }
    if (teacher) {
        params.push(`teacher=${encodeURIComponent(teacher)}`);
    }

    // Добавляем параметры к URL, если они есть
    if (params.length > 0) {
        url += '&' + params.join('&');
    }

    // Выполняем запрос
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка при получении расписания');
            }
            return response.json();
        })
        .then(data => {
            renderSchedule(data.schedule);
            displayedWeek = newWeek; // Обновляем отображаемую неделю
            currentWeekSpan.textContent = displayedWeek; // Обновляем отображение текущей недели
            updateCurrentWeekButton(); // Обновляем кнопку текущей недели
        })
        .catch(error => console.error('Ошибка при получении данных:', error));
}


    // Функция для обновления состояния кнопки текущей недели
    function updateCurrentWeekButton() {
        if (displayedWeek === currentWeek) {
            currentWeekBtn.classList.add('disabled');
        } else {
            currentWeekBtn.classList.remove('disabled');
        }
    }

    // Обработчики кнопок смены недели
    prevWeekBtn.addEventListener('click', () => {
        updateSchedule((displayedWeek - 1 + 20) % 20 || 20); // Переход к предыдущей неделе
    });
    nextWeekBtn.addEventListener('click', () => {
        updateSchedule((displayedWeek % 20) + 1); // Переход к следующей неделе
    });
    currentWeekBtn.addEventListener('click', () => {
        updateSchedule(currentWeek);  // Возвращаемся на текущую неделю
    });
    goToWeekBtn.addEventListener('click', () => {
        const inputWeek = parseInt(weekInput.value);
        if (!isNaN(inputWeek) && inputWeek >= 1 && inputWeek <= 20) {
            updateSchedule(inputWeek);
        }
    });

    // Изначальная загрузка расписания
    fetchSchedule();
});
