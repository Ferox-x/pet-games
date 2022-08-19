from django.urls import path
from api.v1.views import SchulteApiView, StroopApiView

urlpatterns = [
    path('schulte/', SchulteApiView.as_view()),
    path('stroop/', StroopApiView.as_view())
]
