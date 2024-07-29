from django.contrib import admin
from .models import Service, Server, Logs
# Register your models here.
admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Logs)