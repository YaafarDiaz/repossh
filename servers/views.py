from django.shortcuts import render, reverse, HttpResponseRedirect
from .models import Server, ServerForm

def Servers(request):

    title = "Servers"

    context = {
        'title': title,
    }

    return render(request, 'servers/servers.html', context)

def Config(request):
    Servers = Server.objects.all()
    title = "Config"
    form = ServerForm()
    context = {
    'title': title,
    'Servers': Servers,
    'form': form,
    }

    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('config')
            return HttpResponseRedirect(url)   

    return render(request, 'config/config.html', context)
    