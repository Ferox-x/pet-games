from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    """Представление страницы About."""
    template_name = 'about/about.html'
