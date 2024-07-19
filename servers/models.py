from django.db import models
from django import forms

class Service(models.Model):
    name = models.CharField(max_length=20)
    port = models.IntegerField()
    log_path = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class ServiceForm(forms.Form):
    name = forms.CharField(max_length=20)
    port = forms.IntegerField()
    log_path = forms.CharField(max_length=255)

class Server(models.Model):
    user        = models.CharField(max_length=20)
    host_name   = models.CharField(max_length=20)
    ip          = models.CharField(max_length=15)
    password    = models.CharField(max_length=255)

    class Meta:
        ordering = ['ip']

    def __str__(self):
        return self.host_name + ' - ' + self.ip

class ServerForm(forms.Form):
    host_name = forms.CharField(max_length=20)
    ip = forms.CharField(max_length=15)
    log_path = forms.CharField(max_length=255)