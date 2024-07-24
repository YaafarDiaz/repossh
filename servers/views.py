from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from .models import Server, ServerForm, Service, ServiceForm
import paramiko, re

def Servers(request, pk):

    ServerInfo = get_object_or_404(Server, pk=pk)
    Servers = Server.objects.all()
    title = "Servers"
    Services = Service.objects.all()
    ServerName = ServerInfo.host_name
    Results = []


    for service in Services:

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ServerInfo.ip, 22, ServerInfo.user, ServerInfo.password)
        command = "journalctl -u  " +  service.name.casefold()  
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = []

        for line in stdout:
            line = re.sub(r'T', ' ', line)
            line = re.sub(r'\.\d+\+\d{2}:\d{2}', ' ', line)
            lines.append(line)
        
        Results.append(lines)

        ssh.close()

    context = {
        'title': title,
        'Servers': Servers,
        'ServerName': ServerName,
        'Results': Results,
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
    