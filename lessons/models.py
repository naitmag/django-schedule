from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import Group


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
        (0,'8:30-9:50'),
        (1,'10:05-11:25'),
        (2,'12:00-13:20'),
        (3,'13:35-14:55'),
    ]

    day = models.PositiveSmallIntegerField(null=False, blank=False, choices=DAYS, verbose_name='День недели')
    number = models.PositiveSmallIntegerField(null=False, blank=False, choices=TIMES, verbose_name='Номер занятия')
    start = models.PositiveSmallIntegerField(null=False, blank=False, validators=[MinValueValidator(1),MaxValueValidator(20)], verbose_name='Начало')
    end = models.PositiveSmallIntegerField(null=False, blank=False, validators=[MinValueValidator(1),MaxValueValidator(20)], verbose_name='Конец')
    lesson_type = models.CharField(max_length=10, default='-',null=True, blank=False, verbose_name='Тип занятия')
    name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Название')
    teacher = models.CharField(max_length=150, null=False, blank=False, verbose_name='Преподаватель')
    subgroup = models.CharField(max_length=20, null=True, blank=True, verbose_name='Подгруппа')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Группа')

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Занятия'

    def __str__(self):
        return f"[{self.pk}]({self.group.number}) {self.start}-{self.end} {self.lesson_type} {self.name}"

