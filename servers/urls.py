from django.urls import path
from . import views

urlpatterns = [
    path('Config', views.Config, name='config'),
    path('ServerInfo/<int:pk>/', views.Servers, name='ServerInfo'),
]