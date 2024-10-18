document.addEventListener('DOMContentLoaded', function () {
    const scheduleContainer = document.querySelector('.schedule-container');
    const currentWeekSpan = document.getElementById('current-week');
    const prevWeekBtn = document.getElementById('prev-week');
    const nextWeekBtn = document.getElementById('next-week');
    const currentWeekBtn = document.getElementById('current-week-btn');
    const goToWeekBtn = document.getElementById('go-week');
    const weekInput = document.getElementById('week-input');

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const group = urlParams.get('group');
    const teacher = urlParams.get('teacher');

    let currentWeek;
    let displayedWeek;

    function fetchSchedule() {
        let url = '/schedule/get_schedule/';
        const params = [];
        if (group) {
            params.push(`group=${encodeURIComponent(group)}`);
        }
        if (teacher) {
            params.push(`teacher=${encodeURIComponent(teacher)}`);
        }
        if (params.length > 0) {
            url += '?' + params.join('&');
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети при получении расписания');
                }
                return response.json();
            })
            .then(data => {
                currentWeek = data.current_week;
                currentWeekSpan.textContent = currentWeek;
                renderSchedule(data.schedule);
                displayedWeek = currentWeek;
                updateCurrentWeekButton();
            })
            .catch(error => console.error('Ошибка при получении данных:', error));
    }

    function renderSchedule(schedule) {
        scheduleContainer.innerHTML = '';

        schedule.forEach(day => {
            const dayCard = document.createElement('div');
            dayCard.classList.add('schedule-card');

            const cardHeader = document.createElement('header');
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

            cardHeader.textContent = `${day.title} (${day.date})`;
            dayCard.appendChild(cardHeader);

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


                    const subgroupInfo = document.createElement('div');
                    subgroupInfo.classList.add('subgroup-info');
                    subgroupInfo.textContent = lesson.subgroup;
                    lessonDiv.appendChild(subgroupInfo);


                    const lessonExtra = document.createElement('div');
                    lessonExtra.classList.add('lesson-extra');
                    const lessonExtraTrigger = document.createElement('i');
                    lessonExtraTrigger.classList.add('lesson-extra-trigger');
                    lessonExtraTrigger.textContent = 'i';
                    lessonExtra.appendChild(lessonExtraTrigger);

                    const lessonExtraTooltip = document.createElement('div');
                    lessonExtraTooltip.classList.add('lesson-extra-tooltip');

                    const teacherInfo = document.createElement('div');
                    teacherInfo.classList.add('teacher-info');
                    teacherInfo.textContent = lesson.teacher;
                    lessonExtraTooltip.appendChild(teacherInfo);

                    lessonExtra.appendChild(lessonExtraTooltip);
                    lessonDiv.appendChild(lessonExtra);

                    cardBody.appendChild(lessonDiv);
                });
            }

            dayCard.appendChild(cardBody);
            scheduleContainer.appendChild(dayCard);
        });
    }

    function updateSchedule(newWeek) {
        if (newWeek < 1 || newWeek > 20) return;
        let url = `/schedule/get_schedule/?week=${newWeek}`;
        const params = [];
        if (group) params.push(`group=${encodeURIComponent(group)}`);
        if (teacher) params.push(`teacher=${encodeURIComponent(teacher)}`);
        if (params.length > 0) url += '&' + params.join('&');

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети при получении расписания');
                }
                return response.json();
            })
            .then(data => {
                renderSchedule(data.schedule);
                displayedWeek = newWeek;
                currentWeekSpan.textContent = displayedWeek;
                updateCurrentWeekButton();
            })
            .catch(error => console.error('Ошибка при получении данных:', error));
    }

    function updateCurrentWeekButton() {
        if (displayedWeek === currentWeek) {
            currentWeekBtn.classList.add('disabled');
        } else {
            currentWeekBtn.classList.remove('disabled');
        }
    }

    prevWeekBtn.addEventListener('click', () => {
        updateSchedule((displayedWeek - 1 + 20) % 20 || 20);
    });
    nextWeekBtn.addEventListener('click', () => {
        updateSchedule((displayedWeek % 20) + 1);
    });
    currentWeekBtn.addEventListener('click', () => {
        updateSchedule(currentWeek);
    });
    goToWeekBtn.addEventListener('click', () => {
        const inputWeek = parseInt(weekInput.value);
        if (!isNaN(inputWeek) && inputWeek >= 1 && inputWeek <= 20) {
            updateSchedule(inputWeek);
        }
    });

    fetchSchedule();
});
