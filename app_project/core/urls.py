from django.urls import path

from core.views import MainPageView

app_name = 'core'

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
]
