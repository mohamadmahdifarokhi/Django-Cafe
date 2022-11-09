from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
