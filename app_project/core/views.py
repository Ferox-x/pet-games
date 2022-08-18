from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    """Отображение главной страницы."""
    template_name = 'core/main_page/main_page.html'


def page_not_found(request, exception):
    """Отображение ошибки 404."""
    template = 'core/error_page/404.html'
    return render(request, template, {'path': request.path}, status=404)


def server_error(request):
    """Отображение ошибки 500."""
    return render(request, 'core/error_page/500.html', status=500)


def permission_denied(request, exception):
    """Отображение ошибки 403."""
    return render(request, 'core/error_page/403.html', status=403)


def csrf_failure(request, reason=''):
    """Отображение ошибки 403 csrf."""
    return render(request, 'core/error_page/403csrf.html')
