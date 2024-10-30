import datetime
from enum import Enum, auto

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import Group
from lessons.constants import START_LESSONS_DATE, DEFAULT_MAX_WEEK
from datetime import datetime, timedelta


class Week:
    def __init__(self, number: int = None, group: Group = None, teacher: str = None):
        self.number = number or self.get_current_week()
        self.group = group
        self.teacher = teacher
        self.date = START_LESSONS_DATE + timedelta(weeks=int(self.number) - 1)
        if self.group:
            self.lessons = Lesson.objects.filter(group_id=group.pk, start__lte=self.number, end__gte=self.number)
        else:
            self.lessons = Lesson.objects.filter(teacher__icontains=teacher, start__lte=self.number, end__gte=self.number)
        self.lessons = self.lessons.order_by('number')

    @staticmethod
    def get_current_week():
        current_date = datetime.now().date()
        difference = current_date - START_LESSONS_DATE
        current_week = (difference.days + 1) // 7 + 1
        return current_week

    def get_current_lesson(self):
        current_date = datetime.now()
        current_weekday = current_date.weekday()
        lesson_number = Lesson.spot_lesson_number(current_date)
        if lesson_number is None:
            return None

        lesson = self.lessons.filter(day=current_weekday, number=lesson_number).first()
        return lesson

    def get_schedule_json(self, is_teacher=False):
        response_data = {
            'schedule': [],
            'current_week': self.get_current_week()
        }

        for i, day in enumerate(Lesson.DAYS):
            date = self.date + timedelta(days=i)
            content = {
                'title': day[1],
                'date': date.strftime('%d.%m'),
                'lessons': []
            }

            last_lesson = None
            for lesson in self.lessons:
                if i != lesson.day:
                    continue

                teacher_info = f"{lesson.teacher} {lesson.group.number}" if is_teacher else lesson.teacher
                lesson_data = {
                    'id': lesson.pk,
                    'timeSlot': lesson.get_time(),
                    'lesson_type': lesson.lesson_type,
                    'title': lesson.name,
                    'subgroup': lesson.subgroup,
                    'teacher': teacher_info
                }

                if is_teacher and last_lesson and lesson.name == last_lesson.name and \
                        lesson.lesson_type == last_lesson.lesson_type and lesson.number == last_lesson.number:
                    content['lessons'][-1]['teacher'] += f", {lesson.group.number}"
                else:
                    content['lessons'].append(lesson_data)
                    last_lesson = lesson

            response_data['schedule'].append(content)

        return response_data


class LessonRecord:
    def __init__(self, data: list, group: str):
        data = self.parse_lesson(data)
        self.day = data['day']
        self.number = data['number']
        self.weeks = self.parse_weeks(data['weeks'], data['types'])
        self.name = ' '.join(data['name'])
        self.teacher = ' '.join(data['teacher'])
        self.subgroup = data['subgroup']
        self.group = group
        self.raw = data['raw']

    def __str__(self):
        return f"{self.weeks} {self.name} {self.teacher}"

    def get_list(self) -> list:
        result = []
        for item in self.weeks:
            try:
                group = Group.objects.get(number=self.group)
            except Group.DoesNotExist:
                group = Group.objects.create(number=self.group, course=int(self.group[0]), department='Нет информации',
                                             faculty='Нет информации')

            interval = self.parse_interval(item[0])
            lesson = Lesson(
                day=self.day,
                number=self.number,
                start=interval[0],
                end=interval[1],
                lesson_type=item[1],
                name=self.name.capitalize(),
                teacher=self.teacher,
                subgroup=" ".join(self.subgroup),
                group=group
            )
            result.append(lesson)

        return result

    @staticmethod
    def clean_records(data: list | tuple):
        return [item.replace(',', '') for item in data]

    @staticmethod
    def parse_lesson(entry):

        class ArgTypes(Enum):
            WEEKS = auto()
            LESSON_TYPE = auto()
            NAME = auto()
            TEACHER = auto()
            SUBGROUP = auto()

        result = {
            'day': entry[0],
            'number': entry[1],
            'weeks': [],
            'types': [],
            'name': [],
            'subgroup': [],
            'teacher': [],
            'raw': entry
        }

        def detect_type(arg: str):

            if arg.replace(',', '').replace('-', '').isdigit():
                return ArgTypes.WEEKS
            lessons_types = ['лаб.', 'пр.', 'л.', 'сем.']
            if '.' in arg and arg.replace(',', '') in lessons_types:
                return ArgTypes.LESSON_TYPE
            if len(arg) in [4, 5] and arg.upper() == arg and '.' in arg:
                return ArgTypes.TEACHER
            if '(' in arg or ')' in arg:
                return ArgTypes.SUBGROUP
            if arg.upper() == arg and not '.' in arg:
                return ArgTypes.NAME

        search_types = True
        for arg in entry[2:]:
            skip_chars = ['-', '/']
            if not arg in skip_chars:

                arg_type = detect_type(arg)

                if arg_type is ArgTypes.WEEKS:
                    result['weeks'].append(arg)
                elif search_types and arg_type is ArgTypes.LESSON_TYPE:
                    result['types'].append(arg)
                elif arg_type is ArgTypes.NAME:
                    search_types = False
                    result['name'].append(arg)
                elif arg_type is ArgTypes.SUBGROUP:
                    result['subgroup'].append(arg)
                else:
                    result['teacher'].append(arg)
        if not result['weeks']:
            result['weeks'].append(f'1-{DEFAULT_MAX_WEEK}')
        if not result['types']:
            result['types'].append('-')
        return result

    @staticmethod
    def parse_interval(interval: str) -> tuple:
        if not '-' in interval:
            return (int(interval),) * 2

        return tuple(map(int, interval.split('-')))

    def parse_weeks(self, weeks, types):
        n = len(weeks)
        m = len(types)
        result = []

        if not (n > m != 1):
            weeks = self.clean_records(weeks)
            types = self.clean_records(types)

        if n == m:
            result = [(weeks[i], types[i]) for i in range(n)]
        elif n > m:
            if m == 1:
                return [(week, types[0]) for week in weeks]
            else:
                i = 0
                for week in self.clean_records(weeks):
                    if ',' in week and ',' in types[i]:
                        i += 1
                    result.append((week, types[i].replace(',', '')))
        elif n < m:
            if n == 1:
                result.append((weeks[0], '/'.join(types)))
            else:
                for i in range(n):
                    if i == n - 1:
                        result.append((weeks[i], '/'.join(types[n - 1:])))
                        return result
                    result.append((weeks[i], types[i]))
        return result


class Lesson(models.Model):
    DAYS = [
        (0, "Понедельник"),
        (1, "Вторник"),
        (2, "Среда"),
        (3, "Четверг"),
        (4, "Пятница"),
        (5, "Суббота"),
    ]
    TIMES = [
        (0, '8:30 - 9:50'),
        (1, '10:05 - 11:25'),
        (2, '12:00 - 13:20'),
        (3, '13:35 - 14:55'),
    ]
    LESSON_TYPES = [
        ('л.', 'Лекция'),
        ('пр.', 'Практическая'),
        ('лаб.', 'Лабораторная'),
        ('сем.', 'Семинар'),
        ('кардио', 'Кардио'),
        ('силовой', 'Силовой'),
        ('-', 'Не указан'),
    ]

    day = models.PositiveSmallIntegerField(null=False, blank=False, choices=DAYS, verbose_name='День недели')
    number = models.PositiveSmallIntegerField(null=False, blank=False, choices=TIMES, verbose_name='Номер занятия')
    start = models.PositiveSmallIntegerField(null=False, blank=False,
                                             validators=[MinValueValidator(1), MaxValueValidator(20)],
                                             verbose_name='Начало')
    end = models.PositiveSmallIntegerField(null=False, blank=False,
                                           validators=[MinValueValidator(1), MaxValueValidator(20)],
                                           verbose_name='Конец')
    lesson_type = models.CharField(max_length=10, choices=LESSON_TYPES, default='-', null=True, blank=False,
                                   verbose_name='Тип занятия')
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Название')
    teacher = models.CharField(max_length=150, null=False, blank=False, verbose_name='Преподаватель')
    subgroup = models.CharField(max_length=25, null=True, blank=True, verbose_name='Подгруппа')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Группа')

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Занятия'
        verbose_name_plural = 'Занятия'

    def get_time(self):
        return self.TIMES[self.number][1]

    @classmethod
    def spot_lesson_number(cls, time: str | datetime):
        time_format = '%H:%M'
        if isinstance(time, str):
            time = datetime.strptime(time, time_format).time()
        elif isinstance(time, datetime):
            time = time.time()
        else:
            raise ValueError
        for day in cls.TIMES:
            interval = day[1].replace(' ', '').split('-')

            lower = datetime.strptime(interval[0], time_format).time()
            upper = datetime.strptime(interval[1], time_format).time()

            if lower <= time <= upper:
                return day[0]

    def get_day_name(self):
        return self.DAYS[self.day][1]

    def get_group_number(self):
        return self.group.number

    def get_lesson_type(self):
        lessons_order = ['л.', 'пр.', 'лаб.', 'сем.', 'кардио', 'силовой', '-']
        return self.LESSON_TYPES[lessons_order.index(self.lesson_type)][1]

    def __str__(self):
        return f"[{self.pk}]({self.group.number}) {self.start}-{self.end} {self.lesson_type} {self.name}"
