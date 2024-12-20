# Generated by Django 5.1.1 on 2024-11-04 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_student_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="department",
            field=models.CharField(
                default="Нет информации", max_length=150, verbose_name="Кафедра"
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="faculty",
            field=models.CharField(
                default="Нет информации", max_length=150, verbose_name="Факультет"
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="specialization",
            field=models.CharField(
                default="Нет информации", max_length=150, verbose_name="Специализация"
            ),
        ),
    ]
