from django.urls import path

from support.views import SupportView, SupportStaffView, ChangeStatus

app_name = 'support'

urlpatterns = [
    path('', SupportView.as_view(), name='support'),
    path('staff/', SupportStaffView.as_view(), name='support_staff'),
    path('statuschange/', ChangeStatus.as_view())
]
