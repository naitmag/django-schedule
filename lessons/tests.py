from django.test import TestCase

from lessons.services.excel_reader import ExcelReader


class TestExcelReader(TestCase):

    def test_save_lessons(self):
        ExcelReader.save_lessons('data.xlsx')
