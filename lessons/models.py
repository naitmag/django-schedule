from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import Group
from lessons.constants import START_LESSONS_DATE
from datetime import date


class Week:
    def __init__(self, number: int, group: Group = None, teacher: str = None):
        self.number = number
        self.group = group
        self.teacher = teacher
        if self.group:
            self.lessons = Lesson.objects.filter(group_id=group.pk, start__lte=number, end__gte=number)
        else:
            self.lessons = Lesson.objects.filter(teacher__icontains=teacher, start__lte=number, end__gte=number)

    @staticmethod
    def get_current_week():
        current_date = date.today()
        days_difference = current_date.day - START_LESSONS_DATE.day
        current_week = days_difference + 1 // 7
        return current_week

    def get_schedule_json(self):
        response_data = {
            'schedule': [],
            'current_week': self.get_current_week()
        }

        for i in range(len(Lesson.DAYS)):
            content = {
                'title': Lesson.DAYS[i][1],
                'lessons': []
            }
            for lesson in self.lessons:
                if i == lesson.day:
                    value = {
                        'id': lesson.pk,
                        'timeSlot': lesson.get_time(),
                        'lesson_type': lesson.lesson_type,
                        'title': lesson.name,
                        'subgroup': lesson.subgroup,
                        'teacher': lesson.teacher
                    }
                    content['lessons'].append(value)
            response_data['schedule'].append(content)

        return response_data


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
        ('сем.', 'Семинар'),
        ('кардио', 'Кардио'),
        ('силовой', 'Силовой'),
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
    subgroup = models.CharField(max_length=20, null=True, blank=True, verbose_name='Подгруппа')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Группа')

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Занятия'
        verbose_name_plural = 'Занятия'

    def get_time(self):
        return self.TIMES[self.number][1]

    def get_day_name(self):
        return self.DAYS[self.day][1]

    def get_lesson_type(self):
        lessons_order = ['л.', 'пр.', 'сем.', 'кардио', 'силовой']
        return self.LESSON_TYPES[lessons_order.index(self.lesson_type)][1]

    def __str__(self):
        return f"[{self.pk}]({self.group.number}) {self.start}-{self.end} {self.lesson_type} {self.name}"
