from django.shortcuts import render
from django.views import View


class MainPage(View):

    def get(self, request):
        return render(request, 'core/main_page/main_page.html', {})


class ContactsView(View):

    def get(self, request):
        return render(request, 'core/main_page/contacts.html', {})


class AboutView(View):

    def get(self, request):
        return render(request, 'core/main_page/about.html', {})
