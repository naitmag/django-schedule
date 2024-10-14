from django.views.generic import TemplateView
from utils.string_loader import StringLoader


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = StringLoader.get_string('main.title')
        context['email'] = StringLoader.get_string('main.email')
        context['text'] = StringLoader.get_string('main.text')
        return context
