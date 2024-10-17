from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView

from dashboard.forms import CreateUserForm
from users.models import User, Group
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

#TODO
class CreateUserView(FormView):
    template_name = 'dashboard/create_user.html'
    form_class = CreateUserForm  # Укажите вашу форму

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        middle_name = form.cleaned_data['middle_name']
        email = form.cleaned_data['email']
        group = form.cleaned_data['group']

        user = User.objects.create_user(username=username,first_name=first_name, last_name=last_name, middle_name=middle_name,
                                        email=email, group=group)
        user.save()
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
        return f''
