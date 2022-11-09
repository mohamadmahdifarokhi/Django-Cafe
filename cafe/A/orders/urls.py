from django.urls import path, include
from . import views

app_name = 'orders'

# session_urls = [
#     path('set/', views.SetSessionView.as_view(), name='set'),
#     path('delete/', views.DelSessionView.as_view(), name='delete'),
#     path('down/', views.DownSessionView.as_view(), name='down'),
#     path('up/', views.UpSessionView.as_view(), name='up'),
#     path('table/', views.TableSessionView.as_view(), name='table'),
# ]

urlpatterns = [
    path('order', views.OrderView.as_view(), name='order'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    # path('session/', include(session_urls), name='session'),
    path('set/', views.SetSessionView.as_view(), name='set'),
    path('delete/', views.DelSessionView.as_view(), name='delete'),
    path('down/', views.DownSessionView.as_view(), name='down'),
    path('up/', views.UpSessionView.as_view(), name='up'),
    path('table/', views.TableSessionView.as_view(), name='table'),
    path('request/', views.RequestView.as_view(), name='request'),
    path('verify/', views.VerifyView.as_view(), name='verify'),
]
