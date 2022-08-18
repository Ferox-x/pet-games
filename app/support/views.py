from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from services.support_services import Support, SupportStaff, render_support_page
from services.services import is_ajax


class SupportView(View):
    """Отображение для службы поддержки (Обычный пользователь)."""

    def get(self, request):
        if request.user.is_authenticated:
            return render_support_page(request)
        return render(request, 'core/error_page/403.html')

    def post(self, request):

        if request.user.is_authenticated:
            if is_ajax(request):
                json_data = Support(request.user, request.POST).manager()
                return JsonResponse(json_data, status=200)
            Support(request.user, request.POST).manager()
            return redirect('support:support')
        return render(request, 'core/error_page/403.html')


class SupportStaffView(View):
    """Отображение для службы поддержки (Служба поддержки)."""

    def get(self, request):
        if request.user.is_authenticated and request.user.is_support_staff:
            support_staff = SupportStaff(request.user, request.POST)
            tickets = support_staff.get_tickets()
            context = {
                'tickets': tickets,
            }
            return render(request, 'support/support_staff.html', context)
        return render(request, 'core/error_page/403.html')

    def post(self, request):

        if request.user.is_authenticated and request.user.is_support_staff:
            if is_ajax(request):
                json_data = SupportStaff(request.user, request.POST).manager()
                return JsonResponse(json_data, status=200)
            Support(request.user, request.POST).manager()
            return render_support_page(request)

