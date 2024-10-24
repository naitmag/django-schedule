from django.contrib import admin
from django.urls import path

from dashboard.views import DashboardView, CreateUserView, UploadExcelView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name="index"),
    path('create_user/', CreateUserView.as_view(), name="create_user"),
    path('upload_lessons/', UploadExcelView.as_view(), name="upload_lessons"),
]
