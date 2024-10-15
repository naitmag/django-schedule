from django.contrib import admin

from lessons.models import Lesson


# admin.site.register(Lesson)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'day', 'number', 'get_group_number', 'start', 'end']
    search_fields = ['name', 'teacher']
    list_filter = ['name', 'day', 'number', 'start', 'end']

