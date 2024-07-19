from django.shortcuts import render

def Servers(request):

    title = "Servers"

    context = {
        'title': title,
    }

    return render(request, 'servers/servers.html', context)

def Config(request):

    title = "Config"

    context = {
        'title': title,
    }

    return render(request, 'config/config.html', context)