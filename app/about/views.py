from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    """Представление страницы About."""
    template_name = 'about/about.html'


class ContactView(TemplateView):
    """Представление страницы Contacts."""
    template_name = 'about/contacts.html'
