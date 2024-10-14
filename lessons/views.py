import traceback

from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from lessons.models import Lesson, Week
from lessons.services.excel_reader import save_lessons
from users.models import Group
from utils.string_loader import StringLoader


# Create your views here.
class ScheduleView(ListView):
    model = Lesson
    template_name = "lessons/schedule.html"
    context_object_name = "lessons"

    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.GET.get('teacher')
        group = self.request.GET.get('group')

        if teacher and group:
            group = None

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


class GetWeekScheduleView(View):
    def get(self, request):
        week_number = request.GET.get("week") or Week.get_current_week()
        teacher = request.GET.get("teacher")

        if not teacher:
            group_number = request.GET.get('group')
            try:
                if group_number:
                    group = Group.objects.get(number=group_number)
                else:
                    group_id = request.GET.get("group_id") or self.request.user.group.pk
                    group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return JsonResponse({})
            week = Week(week_number, group=group)
        else:
            week = Week(week_number, teacher=teacher)

        response_data = week.get_schedule_json()

        return JsonResponse(response_data)


class UploadExcelView(TemplateView):
    template_name = 'lessons/upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_name = self.request.GET.get('file')

        context['title'] = StringLoader.get_string('lessons.upload.title')
        try:
            file_name += '.xlsx'
            save_lessons(file_name)
        except TypeError:
            context['result'] = StringLoader.get_string('lessons.upload.error')
            context['description'] = StringLoader.get_string('lessons.upload.type_error')
        except Exception as _ex:
            traceback.print_exc()
            context['result'] = StringLoader.get_string('lessons.upload.error')
            context['description'] = _ex
        else:
            context['result'] = StringLoader.get_string('lessons.upload.success')

        return context
