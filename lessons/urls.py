from django.urls import path

from lessons import views

app_name = 'lessons'

urlpatterns = [
    path('', views.ScheduleView.as_view(), name="schedule"),
    path('lesson/<int:lesson_id>', views.LessonView.as_view(), name="lesson"),
    path('get_schedule/', views.GetWeekScheduleView.as_view(), name="get_schedule")
]