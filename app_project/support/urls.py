from django.urls import path

from support.views import SupportView, SupportStaffView

app_name = 'support'

urlpatterns = [
    path('', SupportView.as_view(), name='support'),
    path('staff/', SupportStaffView.as_view(), name='support_staff'),
]
