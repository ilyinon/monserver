from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import ListView, View
from django.http import HttpResponse
from .models import Status, DC, Server
from django.shortcuts import render

from .models import Server, Service, Status
from .serializers import ServerSerializer, ServiceSerializer, StatusSerializer

import logging

from django.template.defaulttags import register


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
    q = Status.objects.all().order_by("server", "service", "-created").distinct("server", "service")
    dcs = DC.objects.all()
    servers = Server.objects.all()
    dc_list = {}
    for dc in dcs:
        dc_list[dc.dc_name] = {}
        counter_server = 0
        counter_bad_server = 0
        for server in servers:
            if server.dc == dc:
                counter_server += 1
                logger.error(server.server_name)
                for status in q:
                    logger.error(status.server)
                    if server == status.server and status.status is False:
                        logger.error(server.server_name)
                        counter_bad_server += 1

        dc_list[dc.dc_name]["servers_all"] = counter_server
        dc_list[dc.dc_name]["servers_bad"] = counter_bad_server
        if counter_bad_server:
            dc_list[dc.dc_name]["status"] = False
        else:
            dc_list[dc.dc_name]["status"] = True

    def get(self, request):
        template_name = 'overall.html'
        return render(request, template_name, context={'all_status': self.dc_list})


class DC_view(View):

    def get(self, request, dc_name):
        dc_name = DC.objects.filter(dc_name=dc_name)[0]
        dc_servers = Server.objects.filter(dc=dc_name)
        template_name = "dc.html"
        return render(request, template_name, context={'dc_name': dc_name, 'dc_servers': dc_servers})

class Server_view(View):

    def get(self, request, server_name):
        server_name = Server.objects.filter(server_name=server_name)[0]
        server_services = Status.objects.all().order_by("server", "service", "-created").distinct("server", "service").\
            filter(server=server_name).values_list("service__service_name", flat=True)
        template_name = "server.html"
        return render(request, template_name, context={'server_name': server_name, 'services': server_services})

class Service_view(View):
    def get(self, request, service_name):
        service = Service.objects.filter(service_name=service_name)
        template_name = "service.html"
        return render(request, template_name, context={"service": service})
