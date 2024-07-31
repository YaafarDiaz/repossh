from django.urls import path
from . import views

urlpatterns = [
    path('Config', views.Config, name='config'),
    path('ServerInfo/<int:pk>/<int:pks>/', views.ServersInfo, name='ServerInfo'),
    path('ServerInfo/', views.Servers, name='Servers'),
    path('Update', views.UpdateLogs, name='UpdateLogs'),
]