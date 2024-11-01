from django.contrib.auth.base_user import BaseUserManager
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

    def get_name(self):
        return f"{self.number} {self.specialization}"

    def __str__(self):
        return f"[{self.pk}] {self.number} {self.specialization}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть установлен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, blank=True, null=False)
    username = None
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"[{self.pk}] {self.get_full_name()} {self.middle_name}"


class Student(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    group: Group = models.ForeignKey(to=Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Группа')

    class Meta:
        db_table = 'student'
        verbose_name = 'Студент'
        verbose_name_plural = 'Студент'

    def __str__(self):
        return f"Студент | {self.user.get_full_name()} {self.user.middle_name}"


class Teacher(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='teacher_images', blank=True, null=True, verbose_name="Аватар")
    position = models.CharField(max_length=50, blank=False, null=False, verbose_name='Должность')
    department = models.CharField(max_length=50, blank=False, null=False, verbose_name='Кафедра')
    faculty = models.CharField(max_length=50, blank=False, null=False, verbose_name='Факультет')

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f"Преподаватель | {self.user.get_full_name()} {self.user.middle_name}"


# TODO
class UserData:
    def __init__(self, user: User):
        self.user = user

        self.first_name = user.first_name
        self.last_name = user.last_name
        self.middle_name = user.middle_name
        self.email = user.email
        self.is_student = user.is_student
        self.is_teacher = user.is_teacher
        self.is_staff = user.is_staff

        if user.is_student:
            self.data = Student.objects.get(user__id=user.pk)
            self.group = self.data.group
            self.department = self.group.department
            self.faculty = self.group.faculty

        elif user.is_teacher:
            self.data = Teacher.objects.get(user__id=user.pk)
            self.image = self.data.image
            self.position = self.data.position
            self.department = self.data.department
            self.faculty = self.data.faculty
