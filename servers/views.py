from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Server, ServerForm, Service, ServiceForm, Logs
import paramiko, re, pytz, logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

@login_required
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

@login_required
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
            messages.success(request, 'Server added successfully!')
            logger.info(f"User {request.user.username} added server: {formserver.cleaned_data['host_name']}")
            url = reverse('config')
            return HttpResponseRedirect(url)

        formservice = ServiceForm(request.POST)
        if formservice.is_valid():
            formservice.save()
            messages.success(request, 'Service added successfully!')
            logger.info(f"User {request.user.username} added service: {formservice.cleaned_data['name']}")
            url = reverse('config')
            return HttpResponseRedirect(url)
        
    else:
        formserver = ServerForm()
        formservice = ServiceForm()

    return render(request, 'config/config.html', context)
    
@login_required
def UpdateLogs(request):
    Servers = Server.objects.all()
    Services = Service.objects.all()
    
    updated_count = 0
    error_count = 0
    
    for server in Servers:
        for service in Services:
            try:   
                ssh = paramiko.SSHClient()
                # Better SSH security policy (still auto-add but log it)
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                # Use decrypted password
                decrypted_password = server.get_decrypted_password()
                ssh.connect(server.ip, 22, server.user, decrypted_password, timeout=10)
                
                logger.info(f"Connected to {server.host_name} ({server.ip}) for service {service.name}")
                
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
                        updated_count += 1
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
                            updated_count += 1
            
                ssh.close()
                logger.info(f"Successfully updated logs from {server.host_name} for {service.name}")

            except paramiko.AuthenticationException as e:
                error_count += 1
                logger.error(f"Authentication failed for {server.host_name} ({server.ip}): {str(e)}")
                messages.error(request, f'Authentication failed for {server.host_name}')
            except paramiko.SSHException as e:
                error_count += 1
                logger.error(f"SSH error for {server.host_name} ({server.ip}): {str(e)}")
                messages.error(request, f'SSH error for {server.host_name}: {str(e)}')
            except Exception as error:
                error_count += 1
                logger.error(f"Update error for {server.host_name} - {service.name}: {str(error)}")
                messages.error(request, f'Error updating {server.host_name}: {str(error)}')

    if updated_count > 0:
        messages.success(request, f'Successfully updated {updated_count} log entries')
    if error_count > 0:
        messages.warning(request, f'{error_count} errors occurred during update')
    
    logger.info(f"User {request.user.username} updated logs. Updated: {updated_count}, Errors: {error_count}")
    return redirect('Servers')

@login_required
def Servers(request):
    if Service.objects.first():
        FirtsService = Service.objects.first()
    else:
        return redirect('config')
    
    Servers = Server.objects.all()
    context = {'title': "Servers", 'Servers': Servers, 'service': FirtsService.id }
    return render(request, 'servers/serversInfo.html', context)