from django.contrib.auth.models import AbstractUser
from django.db import models


class Group(models.Model):
    number = models.CharField(max_length=10, unique=True, verbose_name='Группа')
    course = models.PositiveSmallIntegerField(default=1, verbose_name='Курс')
    specialization = models.CharField(max_length=150, unique=False, verbose_name='Специализация')
    department = models.CharField(max_length=150, blank=False, null=False, verbose_name='Кафедра')
    faculty = models.CharField(max_length=150, blank=False, null=False, verbose_name='Факультет')

    class Meta:
        db_table = 'group'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return f"[{self.pk}] {self.number} {self.specialization}"


class User(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True, null=False)
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name="Аватар")
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Группа')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"[{self.pk}] {self.username}"

