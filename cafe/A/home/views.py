from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')


class MenuView(View):
    def get(self, request):
        return render(request, 'home/home.html')


class ProfileView(View):
    def get(self, request):
        return render(request, 'home/home.html')
