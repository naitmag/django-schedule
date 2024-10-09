from collections import defaultdict

from django.db.models import QuerySet
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from lessons.models import Lesson, Week
from lessons.services.excel_reader import save_lessons
from users.models import Group


# Create your views here.
class ScheduleView(ListView):
    model = Lesson
    template_name = "lessons/schedule.html"
    context_object_name = "lesson"

    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Расписание"
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


class GetWeekScheduleView(View):
    def get(self, request):
        week_number = request.GET.get("week") or Week.get_current_week()
        teacher = request.GET.get("teacher")

        if not teacher:
            group_id = request.GET.get("group_id") or self.request.user.group.pk
            group = Group.objects.get(id=group_id)
            week = Week(week_number, group=group)
        else:
            week = Week(week_number, teacher=teacher)

        response_data = week.get_schedule_json()

        return JsonResponse(response_data)

class UploadExcelView(TemplateView):
    template_name = 'lessons/upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Загрузка занятий'
        context['read_result'] = save_lessons()
        return context

