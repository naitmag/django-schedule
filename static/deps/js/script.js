    const colors = ['#8cbfba', '#8aacc8', '#d4c56e', '#d89e9f', '#c2a49c', '#a49bd8'];
    const footerColor = colors[Math.floor(Math.random() * colors.length)];
    document.documentElement.style.setProperty('--random-color', footerColor);

function toggleMenu() {
        const sidebar = document.getElementById('sidebar');
        const isOpen = sidebar.style.left === '0px';
        sidebar.style.left = isOpen ? '-250px' : '0px'; // Скрываем/показываем меню
        document.body.style.marginLeft = isOpen ? '0' : '250px'; // Сдвигаем контент
    }

let currentWeek = 1
    let weekOnPage = 4; // Начальная неделя

    // Функция для изменения учебной недели
    function changeWeek(direction) {
        weekOnPage += direction;
        document.getElementById('current-week').innerText = `Неделя ${weekOnPage} (23.09 - 29.09)`; // Обновление текста с номером недели и датами

        // Проверка на текущую неделю
        if (weekOnPage !== currentWeek) {
            document.getElementById('nearest-week').style.display = 'inline-block';
        } else {
            document.getElementById('nearest-week').style.display = 'none';
        }
    }