import traceback

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, FormView

from dashboard.forms import CreateStudentForm, CreateTeacherForm
from dashboard.utils import generate_password, share_user_password
from lessons.services.excel_reader import ExcelReader
from users.models import User, Group, Student, Teacher
from utils.string_loader import StringLoader


class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = StringLoader.get_string('dashboard.title')
        return context


# TODO
class CreateStudentView(FormView):
    template_name = 'dashboard/create_student.html'
    form_class = CreateStudentForm

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        middle_name = form.cleaned_data['middle_name']
        email = form.cleaned_data['email']
        group = form.cleaned_data['group']

        user_password = generate_password()
        try:
            with transaction.atomic():
                user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                middle_name=middle_name,
                                                email=email, is_student=True, password=user_password)

                Student.objects.create(user=user, group=group)
        except Exception as e:
            messages.error(self.request, e)
        else:
            share_user_password(user, user_password)
            messages.success(self.request, 'Успешная регистрация пользователя!')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context

    def get_success_url(self):
        return ''


class CreateTeacherView(FormView):
    template_name = 'dashboard/create_teacher.html'
    form_class = CreateTeacherForm

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        middle_name = form.cleaned_data['middle_name']
        email = form.cleaned_data['email']
        position = form.cleaned_data['position']
        department = form.cleaned_data['department']
        faculty = form.cleaned_data['faculty']

        user_password = generate_password()
        try:
            with transaction.atomic():
                user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                                middle_name=middle_name,
                                                email=email, is_teacher=True, password=user_password)

                Teacher.objects.create(user=user, position=position, department=department, faculty=faculty)
        except Exception as e:
            messages.error(self.request, e)
        else:
            share_user_password(user, user_password)
            messages.success(self.request, 'Успешная регистрация пользователя!')

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context

    def get_success_url(self):
        return ''


class UploadExcelView(TemplateView, View):
    template_name = 'dashboard/upload_lessons.html'

    def post(self, request):
        context = super().get_context_data()
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            try:
                ExcelReader.save_lessons(uploaded_file)
            except TypeError:
                context['result'] = StringLoader.get_string('lessons.upload.error')
                context['description'] = StringLoader.get_string('lessons.upload.type_error')
            except Exception as _ex:
                traceback.print_exc()
                context['result'] = StringLoader.get_string('lessons.upload.error')
                context['description'] = _ex
            else:
                context['result'] = StringLoader.get_string('lessons.upload.success')
        else:
            return HttpResponse("Ошибка: файл не был загружен")
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = StringLoader.get_string('lessons.upload.title')

        return context
