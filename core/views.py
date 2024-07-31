from django.shortcuts import render, redirect
from servers.models import Server, Service

def home(request):
    Servers = Server.objects.all()
    if Service.objects.first():
        FirtsService = Service.objects.first()
    else:
        return redirect('config')

    context = {
        'service': FirtsService.id,
        'title': "Home",
        'Servers': Servers,
    }
    return render(request, 'core/index.html', context)