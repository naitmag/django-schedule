import traceback

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, FormView

from dashboard.forms import CreateUserForm
from dashboard.utils import generate_password, share_user_password
from lessons.services.excel_reader import save_lessons
from users.models import User, Group, Student
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
    template_name = 'dashboard/create_user.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        middle_name = form.cleaned_data['middle_name']
        email = form.cleaned_data['email']
        group = form.cleaned_data['group']

        user = User.objects.create_user(first_name=first_name, last_name=last_name,
                                        middle_name=middle_name,
                                        email=email, is_student=True)

        random_password = generate_password()

        user.set_password(random_password)
        user.save()
        student = Student.objects.create(user=user, group=group)
        student.save()

        share_user_password(user, random_password)
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
                save_lessons(uploaded_file)
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
