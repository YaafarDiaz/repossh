from django.contrib import admin
from .models import Service, Server
# Register your models here.
admin.site.register(Server)
admin.site.register(Service)