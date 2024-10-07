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
