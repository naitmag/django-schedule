from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, DetailView, ListView

from users.forms import UserLoginForm
from users.models import User, Group


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    # success_url = reverse_lazy('main:index')
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page

        return reverse_lazy('main:index')

    def form_valid(self, form):

        user = form.get_user()
        if user:
            auth.login(self.request, user)

            return HttpResponseRedirect(self.get_success_url())


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    id_kwarg = "user_id"

    def get_object(self, queryset=None):
        kwarg = self.kwargs.get(self.id_kwarg)
        if not kwarg:
            return self.request.user

        try:
            user = User.objects.get(id=kwarg)
        except User.DoesNotExist:
            raise Http404("User does not exist")

        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'

        return context


class UserRegistrationView(TemplateView):
    template_name = 'users/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


class GroupsListView(ListView):
    model = Group
    template_name = "users/groups.html"
    context_object_name = "groups"

    def get_queryset(self):
        groups = super().get_queryset()
        return groups

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Список групп"
        return context
