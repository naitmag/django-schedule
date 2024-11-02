from django.test import TestCase

from lessons.services.excel_reader import save_lessons


class TestExcelReader(TestCase):

    def test_save_lessons(self):
        save_lessons('data.xlsx')
