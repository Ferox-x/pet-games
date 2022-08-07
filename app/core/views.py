from django.shortcuts import render
from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    template_name = 'core/main_page/main_page.html'


def page_not_found(request, exception):
    template = 'core/error_page/404.html'
    return render(request, template, {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'core/error_page/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'core/error_page/403.html', status=403)


def csrf_failure(request, reason=''):
    return render(request, 'core/error_page/403csrf.html')
