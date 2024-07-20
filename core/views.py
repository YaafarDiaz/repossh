from django.shortcuts import render
from servers.models import Server

def home(request):

    title = "Home"
    Servers = Server.objects.all()

    context = {
        'title': title,
        'Servers': Servers,
    }
    return render(request, 'core/index.html', context)