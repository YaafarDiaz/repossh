from django.shortcuts import render, reverse, HttpResponseRedirect
from .models import Server, ServerForm, Service, ServiceForm

def Servers(request):
    Servers = Server.objects.all()
    title = "Servers"

    context = {
        'Servers': Servers,
        'title': title,
    }

    return render(request, 'servers/servers.html', context)

def Config(request):
    title = "Config"
    Servers = Server.objects.all()
    formserver = ServerForm()
    Services = Service.objects.all()
    formservice = ServiceForm()
    context = {
    'title': title,
    'Servers': Servers,
    'formserver': formserver,
    'Services': Services,
    'formservice': formservice,
    }

    if request.method == 'POST':
        formserver = ServerForm(request.POST)
        if formserver.is_valid():
            formserver.save()
            url = reverse('config')
            return HttpResponseRedirect(url)

        formservice = ServiceForm(request.POST)
        if formservice.is_valid():
            formservice.save()
            url = reverse('config')
            return HttpResponseRedirect(url)
        
    else:
        formserver = ServerForm()
        formservice = ServiceForm()

    return render(request, 'config/config.html', context)
    