from django.db import models
from django import forms
from .encryption import encrypt_password, decrypt_password

class Service(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Server(models.Model):
    user        = models.CharField(max_length=20)
    host_name   = models.CharField(max_length=20)
    ip          = models.CharField(max_length=15)
    password    = models.CharField(max_length=500)  # Aumentado para contraseñas encriptadas

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.host_name + ' - ' + self.ip
    
    def save(self, *args, **kwargs):
        """Override save to encrypt password before saving"""
        if self.password and not self.password.startswith('gAAAAA'):  # Check if already encrypted
            self.password = encrypt_password(self.password)
        super().save(*args, **kwargs)
    
    def get_decrypted_password(self):
        """Get decrypted password for SSH connection"""
        return decrypt_password(self.password)

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['user', 'host_name', 'ip', 'password']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'render_value': False}),
        }

class Logs(models.Model):
    host_name   = models.CharField(max_length=20)
    date        = models.DateTimeField()
    service     = models.CharField(max_length=100)
    message     = models.CharField(max_length=400)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.host_name + ' - ' + self.service
