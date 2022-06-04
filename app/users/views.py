from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views import View


class Login(LoginView):

    template_name = 'auth/login.html'


class Logout(LogoutView):

    next_page = '/'


class ProfileView(View):

    def get(self, request):
        return render(request, 'auth/profile.html')


class RegisterView(View):

    def get(self, request):
        return render(request, 'auth/register.html')
