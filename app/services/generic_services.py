def is_ajax(request):
    """Метод проверяющий запрос на ajax."""
    return request.POST.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
