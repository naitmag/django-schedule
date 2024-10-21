from django.contrib import admin
from django.urls import path

from dashboard.views import DashboardView, CreateStudentView, UploadExcelView, CreateTeacherView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="index"),
    path('create_student/', CreateStudentView.as_view(), name="create_student"),
    path('create_teacher/', CreateTeacherView.as_view(), name="create_teacher"),
    path('upload_lessons/', UploadExcelView.as_view(), name="upload_lessons"),
]
