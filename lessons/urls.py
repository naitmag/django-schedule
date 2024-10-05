from django.urls import path

from lessons import views

app_name = 'lessons'

urlpatterns = [
    path('', views.ScheduleView.as_view(), name="schedule")
]
