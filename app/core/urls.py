from django.urls import path

from core.views import MainPage, ContactsView, AboutView


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('about/', AboutView.as_view(), name='about'),
]