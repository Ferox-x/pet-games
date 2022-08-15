from django.urls import path

from support.views import SupportView

app_name = 'support'

urlpatterns = [
    path('', SupportView.as_view(), name='support'),
]
