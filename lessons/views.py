from collections import defaultdict

from django.db.models import QuerySet
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView

from lessons.models import Lesson


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
        week_number = request.GET.get("week_number")

        lessons = Lesson.objects.filter(start__lte=week_number, end__gte=week_number)

        schedule = defaultdict(lambda: defaultdict(list))

        for lesson in lessons:
            schedule[lesson.get_day_name()][lesson.get_time()].append({
                'id': lesson.pk,
                'lesson_type': lesson.lesson_type,
                'name': lesson.name,
                'teacher': lesson.teacher,
                'subgroup': lesson.subgroup,
            })
        #temp value
        max_week = 20

        response_data = {
            'schedule': dict(schedule),
            'max_week': max_week
        }

        return JsonResponse(response_data)
