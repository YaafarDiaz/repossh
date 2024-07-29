from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404, redirect
from .models import Server, ServerForm, Service, ServiceForm, Logs
import paramiko, re, pytz
from datetime import datetime

def Servers(request, pk):

    ServerInfo = get_object_or_404(Server, pk=pk)
    Servers = Server.objects.all()
    title = "Servers"
    Services = Service.objects.all()
    ServerName = ServerInfo.host_name
    Results = []


    for service in Services:
        try:
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
        except Exception as error:
            message = "Error"

    context = {
        'Services': Services,
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
    
def UpdateLogs(request):
    Servers = Server.objects.all()
    Services = Service.objects.all()
    
    for server in Servers:

        for service in Services:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(server.ip, 22, server.user, server.password)
                command = "journalctl -u  " +  service.name.casefold()  
                stdin, stdout, stderr = ssh.exec_command(command)
                LastUpdate = Logs.objects.filter(service=service.name).latest('date')
                
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
                message = "Error"

        return redirect('ServerInfo')