from django.http import JsonResponse, Http404
from django.views import View
from django.views.generic import ListView, DetailView

from lessons.models import Lesson, Week
from users.models import Group, UserData
from utils.string_loader import StringLoader


# Create your views here.
class ScheduleView(ListView):
    model = Lesson
    template_name = "lessons/schedule.html"
    context_object_name = "lessons"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.GET.get('teacher')
        group = self.request.GET.get('group')

        if teacher and group:
            group = None

        user_data = UserData(self.request.user)
        context['user_data'] = user_data

        context["teacher"] = teacher
        context["group"] = group
        context["title"] = StringLoader.get_string('lessons.schedule.title')

        return context


class LessonView(DetailView):
    template_name = 'lessons/lesson.html'
    id_url_kwarg = 'lesson_id'
    context_object_name = 'lesson'

    def get_object(self, queryset=None):
        return Lesson.objects.get(id=self.kwargs.get(self.id_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object.teacher
        context['related_lessons'] = Lesson.objects.filter(teacher__icontains=teacher).exclude(id=self.object.id)
        context['title'] = self.object.name
        return context


# TODO
class GetWeekScheduleView(View):
    def get(self, request):
        week_number = request.GET.get("week")
        teacher: str = request.GET.get("teacher")
        group_number = request.GET.get('group')

        if teacher and group_number:
            return Http404()

        if group_number:
            try:
                group = Group.objects.get(number=group_number)
            except Group.DoesNotExist:
                return Http404()
            week = Week(week_number, group=group)
        elif teacher:
            week = Week(week_number, teacher=teacher)
        else:
            if self.request.user.is_teacher:
                week = Week(week_number, teacher=self.request.user.last_name)
            elif self.request.user.is_student:
                user_data = UserData(self.request.user)
                week = Week(week_number, group=user_data.group)

        response_data = week.get_schedule_json((self.request.user.is_teacher and not group_number) or teacher)

        return JsonResponse(response_data)
