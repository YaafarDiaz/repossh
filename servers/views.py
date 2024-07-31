from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404, redirect
from .models import Server, ServerForm, Service, ServiceForm, Logs
import paramiko, re, pytz
from datetime import datetime

def ServersInfo(request, pk, pks):
    ServerInfo = get_object_or_404(Server, pk=pk)    
    ServiceToLoad = get_object_or_404(Service, pk=pks)
    Servers = Server.objects.all()
    title = "Servers"
    Services = Service.objects.all()
    Results = []
    if Service.objects.first():
        FirtsService = Service.objects.first()
    else:
        return redirect('config')

    Results.append(Logs.objects.filter(service= ServiceToLoad.name))
 
    context = {
        'service': FirtsService.id,
        'ServiceToLoad': ServiceToLoad,
        'Services': Services,
        'title': title,
        'Servers': Servers,
        'ServerInfo': ServerInfo,
        'Results': Results,
    }

    return render(request, 'servers/servers.html', context)

def Config(request):
    title = "Config"
    Servers = Server.objects.all()
    formserver = ServerForm()
    Services = Service.objects.all()
    formservice = ServiceForm()
    FirtsService = Service.objects.first()
    context = {
    'title': title,
    'Servers': Servers,
    'formserver': formserver,
    'Services': Services,
    'formservice': formservice,
    'service': FirtsService.id,
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
    
def UpdateLogs(request):
    Servers = Server.objects.all()
    Services = Service.objects.all()
    
    for server in Servers:

        for service in Services:
            try:   
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(server.ip, 22, server.user, server.password)
                command = "journalctl -u  " +  service.name.casefold() + "| grep ^[A-Z]" 
                stdin, stdout, stderr = ssh.exec_command(command)

                queryset = Logs.objects.filter(service=service.name)

                if not queryset.exists():   
                    for line in stdout:
                        line = re.sub(r'T', ' ', line)
                        line = re.sub(r'\.\d+\+\d{2}:\d{2}', ' ', line)
                        parts = line.split()
                        date_time = f"{parts[0]} {parts[1]} {parts[2]}"
                        rest_of_string = line[len(date_time):].strip()
                        server_name = rest_of_string.split(' ', 1)[0]
                        system_message = rest_of_string[len(server_name):].strip()
                        date_time = f'{date_time} {datetime.now().year}'
                        date_time = datetime.strptime(date_time, '%b %d %H:%M:%S %Y')
                        date_time = pytz.timezone('America/Bogota').localize(date_time)
                        reg = Logs(host_name=server_name, date=date_time, service=service.name, message=system_message)
                        reg.save()
                else:
                    LastUpdate = queryset.latest('date')
                    for line in stdout:
                        line = re.sub(r'T', ' ', line)
                        line = re.sub(r'\.\d+\+\d{2}:\d{2}', ' ', line)
                        parts = line.split()
                        date_time = f"{parts[0]} {parts[1]} {parts[2]}"
                        rest_of_string = line[len(date_time):].strip()
                        server_name = rest_of_string.split(' ', 1)[0]
                        system_message = rest_of_string[len(server_name):].strip()
                        date_time = f'{date_time} {datetime.now().year}'
                        date_time = datetime.strptime(date_time, '%b %d %H:%M:%S %Y')
                        date_time = pytz.timezone('America/Bogota').localize(date_time)
                        reg = Logs(host_name=server_name, date=date_time, service=service.name, message=system_message)
                        if date_time > LastUpdate.date:
                            reg.save()
            
                ssh.close()

            except Exception as error:
                print("Update Error")

    return redirect('Servers')

def Servers(request):
    if Service.objects.first():
        FirtsService = Service.objects.first()
    else:
        return redirect('config')
    
    Servers = Server.objects.all()
    context = {'title': "Servers", 'Servers': Servers, 'service': FirtsService.id }
    return render(request, 'servers/serversInfo.html', context)