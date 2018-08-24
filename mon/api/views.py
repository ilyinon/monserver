from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import ListView, View
from django.http import HttpResponse
from .models import Status, DC, Server, Lab
from django.shortcuts import render

from .models import Server, Service, Status
from .serializers import ServerSerializer, ServiceSerializer, StatusSerializer

import logging

from django.template.defaulttags import register
from datetime import datetime, timedelta
import pytz


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


logger = logging.getLogger(__name__)

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class StatusRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.all()


class Overview(View):

    @register.filter
    def get(self, request):
        q = Status.objects.all().order_by("server", "service", "-created").distinct("server", "service")
        labs = Lab.objects.all().exclude(pk=99)
        servers = Server.objects.all()
        lab_list = {}

        time_threshold = pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=2)

        for lab in labs:
            lab_list[lab.lab_name] = {}
            counter_server = 0
            counter_bad_server = 0
            for server in servers:
                if server.lab == lab:
                    counter_server += 1
#                   logger.error(server.server_name)
                    for status in q:
#                       logger.error(status.server)
                        if server == status.server and status.status is False or server == status.server and status.updated < time_threshold:
#                           logger.error(server.server_name)
                            counter_bad_server += 1

            lab_list[lab.lab_name]["servers_all"] = counter_server
            lab_list[lab.lab_name]["servers_bad"] = counter_bad_server
            if counter_bad_server:
                lab_list[lab.lab_name]["status"] = False
            else:
                lab_list[lab.lab_name]["status"] = True
        template_name = 'overall.html'
        return render(request, template_name, context={'all_status': lab_list})


class DC_view(View):

    def get(self, request, dc_name):
        dc_name = DC.objects.filter(dc_name=dc_name)[0]
        dc_servers = Server.objects.filter(dc=dc_name)
        template_name = "dc.html"
        return render(request, template_name, context={'dc_name': dc_name, 'dc_servers': dc_servers})


class LAB_view(View):
    @register.filter
    def get(self, request, lab_name):
        lab_name = Lab.objects.filter(lab_name=lab_name)[0]
        lab_servers = Server.objects.filter(lab=lab_name)
        lab_servers_all = {}
        for server in lab_servers:
            lab_servers_all[server] = 0
            services = Status.objects.all().order_by("server", "service", "-created").\
                distinct("server", "service").filter(server=server).values_list("service__service_name", "version")
            lab_servers_all[server] = services

        template_name = "lab.html"
        return render(request, template_name, context={'lab_name': lab_name,
                                                       'lab_servers': lab_servers_all,
                                                       'services_all': lab_servers_all})


class Server_view(View):

    def get(self, request, server_name):
        server_name = Server.objects.filter(server_name=server_name)[0]
        server_services = Status.objects.all().order_by("server", "service", "-updated")\
            .distinct("server", "service").\
            filter(server=server_name).values_list("service__service_name", "version")
        template_name = "server.html"
        return render(request, template_name, context={'server_name': server_name, 'services': server_services})


class Service_view(View):
    def get(self, request, server_name, service_name):
        service = Service.objects.filter(service_name=service_name)
        server = Server.objects.filter(server_name=server_name)
        status_service = Status.objects.filter(service=service[0],server=server[0]).values_list("status", "version", "updated")
        template_name = "service.html"
        return render(request, template_name, context={"status_service": status_service})


class Version_view(View):
    def get(self, request):
        statuses = Status.objects.all().order_by("server", "service", "-created").distinct("server", "service")
        labs = Lab.objects.all().exclude(pk=99)
        data_list = {}
        service_list = {}
        servers = Server.objects.all()
        for lab in labs:
            data_list[lab] = {}
            for server in servers:
                if server.lab == lab:
                    data_list[lab][server.server_name] = {}
        for status in statuses:
            for lab in data_list:
                service_list[lab] = {}
                version_list = []
                for server in data_list[lab]:
                    if server == status.server.server_name:
                        version_list.append(status.version)
                service_list[lab][status.service.service_name] = version_list

        services = Service.objects.all()
        template_name = "version.html"
        return render(request, template_name, context={'data': service_list,
                                                       'services': services},)
