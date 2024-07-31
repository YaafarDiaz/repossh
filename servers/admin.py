from django.contrib import admin
from .models import Service, Server, Logs


@admin.register(Server)
class ServersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'host_name', 'ip', 'password') 
    list_filter = ('user', 'host_name', 'ip', 'user')
    search_fields = ('host_name', 'user')    


@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    list_filter = ('id', 'name')
    search_fields = ('id', 'name') 

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'date', 'message') 
    list_filter = ('service', 'date')
    search_fields = ('service', 'message') 