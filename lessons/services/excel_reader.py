from typing import Any

import pandas as pd
from django.db import transaction

from lessons.models import LessonRecord, Lesson
from users.models import Group


# TODO
class ExcelReader:
    TIMES = ['8.30\n9.50', '10.05\n11.25', '12.00\n13.20', '13.35\n14.55']
    DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

    @staticmethod
    def get_groups(data: Any):
        for i in range(len(data)):
            if data[i][0] == '' and data[i][1] == 'время':
                groups = data[i]
                groups = [s.strip() for s in groups]
                groups = [item for item in groups if item not in ['', 'время']]
                return groups, i

    @classmethod
    def read_excel_data(cls, file):
        df = pd.read_excel(file)
        df = df.fillna('')

        data = df.to_numpy()
        groups, groups_line = cls.get_groups(data)

        schedule = {group: [] for group in groups}

        lesson_day = 0
        lesson_number = 0
        for target_step in data[groups_line + 1:]:
            group_number = 0
            guess_day = target_step[0].replace(' ', '')
            guess_time = target_step[1].replace(' ', '')
            if guess_day in cls.DAYS:
                lesson_day = cls.DAYS.index(guess_day)
            if guess_time in cls.TIMES:
                lesson_number = cls.TIMES.index(guess_time)

            for i in range(2, len(target_step)):
                item = target_step[i]
                if item:
                    if i >= len(target_step) - 2:
                        group_number = 0
                    else:
                        schedule[groups[group_number]].append(f"{lesson_day} {lesson_number} {item}")
                        group_number += 1
                else:
                    group_number += 1

        return groups, schedule

    @classmethod
    def save_lessons(cls, file: str):
        groups, schedule = cls.read_excel_data(file)

        groups_objects = {}
        for group in groups:
            try:
                groups_objects[group] = Group.objects.get(number=group)
            except Group.DoesNotExist:
                groups_objects[group] = Group.objects.create(number=group, course=int(group[0]))
        lessons_to_create = []
        try:
            with transaction.atomic():
                for group in groups:
                    result = schedule[group]

                    for item in result:
                        data = item.split()
                        record = LessonRecord(data, groups_objects[group])
                        result = record.get_list()

                        for lesson in result:
                            lessons_to_create.append(lesson)
                Lesson.objects.bulk_create(lessons_to_create)
        except Exception as e:
            raise e

    print("LESSONS SAVED!")
