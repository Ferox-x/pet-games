from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, reverse_lazy

from . import views
from .views import ProfileView

app_name = 'users'

urlpatterns = [
    path('signup/', views.CustomSignupView.as_view(
        template_name='registration/signup.html'),
         name='signup'
         ),
    path('login/', views.CustomLoginView.as_view(
        template_name='registration/login.html'),
         name='login'
         ),
    path('logout/', views.logout,
         name='logout'),
    path('password_change/', views.CustomPasswordsChangeView.as_view(
        template_name='registration/change_password.html'),
         name='password_change'
         ),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'),
         name='password_change_done'
         ),
    path('password_reset/', views.CustomPasswordResetView.as_view(
        template_name='registration/password_reset_form.html'),
         name='password_reset'
         ),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'
         ),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'
         ),
    path('profile/', ProfileView.as_view())
]
