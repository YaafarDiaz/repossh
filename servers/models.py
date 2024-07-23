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

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'port', 'log_path']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'port': forms.NumberInput(attrs={'class': 'form-control'}),
            'log_path': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Server(models.Model):
    user        = models.CharField(max_length=20)
    host_name   = models.CharField(max_length=20)
    ip          = models.CharField(max_length=15)
    password    = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.host_name + ' - ' + self.ip

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['user', 'host_name', 'ip', 'password']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }