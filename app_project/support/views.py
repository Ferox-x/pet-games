from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from services.generic_services import is_ajax
from services.support_services import Support, SupportStaff


class SupportView(View):
    """Отображение для службы поддержки (Обычный пользователь)."""

    def get(self, request):
        support = Support(request.user, request.POST)
        tickets = support.get_tickets()
        context = {
            'tickets': tickets,
        }
        return render(request, 'support/support.html', context)

    def post(self, request):
        if is_ajax(request):
            json_data = Support(request.user, request.POST).manager()
            return JsonResponse(json_data, status=200)
        Support(request.user, request.POST).manager()
        return redirect('support:support')


class SupportStaffView(View):
    """Отображение для службы поддержки (Служба поддержки)."""

    def get(self, request):
        if request.user.is_support_staff or request.user.is_superuser:
            support_staff = SupportStaff(request.user, request.POST)
            tickets = support_staff.get_tickets()
            context = {
                'tickets': tickets,
            }
            return render(request, 'support/support.html', context)

    def post(self, request):
        if request.user.is_support_staff:
            if is_ajax(request):
                json_data = SupportStaff(request.user, request.POST).manager()
                return JsonResponse(json_data, status=200)
