from django.urls import path
from . import views

urlpatterns = [
    path('Config', views.Config, name='config'),
    path('Servers', views.Servers, name='Servers'),
]