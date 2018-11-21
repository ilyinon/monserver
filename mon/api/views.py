from rest_framework import generics
from django.views.generic import View
from django.shortcuts import render, redirect

from .models import Server, Service, Status, Report, Lab, DC, Winnode
from .serializers import StatusSerializer

import logging
import pytz

from datetime import datetime, timedelta

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


logger = logging.getLogger(__name__)


class ServersAll(View):
    def get(self, request):
        queryset = Server.objects.all()
        template_name = 'servers.html'
        return render(request, template_name, context={'all': queryset})


class ServicesAll(View):
    def get(self, request):
        queryset = Service.objects.all()
        template_name = 'services.html'
        return render(request, template_name, context={'all': queryset})


class StatusRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.all()


class Overview(View):

    @register.filter
    def get(self, request):
        q = Report.objects.all()
        labs = Lab.objects.all().exclude(pk=99)
        report = {}
        for lab in labs:
            report[lab.lab_name] = {}
            report[lab.lab_name]["servers"] = 0
            report[lab.lab_name]["fail"] = 0
            report[lab.lab_name]["serverwservices"] = 0
            for server in q:
                if server.lab == lab:
                    report[lab.lab_name]["servers"] += 1
                    if not server.status or server.status == "no_data":
                        report[lab.lab_name]["fail"] += 1
                    if server.service.service_name != "UNKNOWN":
                        report[lab.lab_name]["serverwservices"] += 1

        template_name = 'overall.html'
        return render(request, template_name, context={'all_status': report})


class DC_view(View):

    def get(self, request, dc_name):
        try:
            dc_name = DC.objects.filter(dc_name=dc_name)[0]
        except:
            return redirect('/')
        dc_servers = Server.objects.filter(dc=dc_name)
        template_name = "dc.html"
        return render(request, template_name, context={'dc_name': dc_name, 'dc_servers': dc_servers})


class LAB_view(View):
    @register.filter
    def get(self, request, lab_name):
        try:
            lab_name = Lab.objects.filter(lab_name=lab_name)[0]
        except:
            return redirect('/')

        lab_servers = Report.objects.filter(lab=lab_name).exclude(service=99).order_by('service__service_name')

        template_name = "lab.html"
        return render(request, template_name, context={'lab_name': lab_name,
                                                       'lab_servers': lab_servers})


class Server_view(View):

    def get(self, request, server_name):
        try:
            server_name = Server.objects.filter(server_name=server_name)[0]
        except:
            return redirect('/')
        server_services = Status.objects.all().order_by("server", "service", "-updated")\
            .distinct("server", "service").\
            filter(server=server_name).values_list("service__service_name", "version")
        template_name = "server.html"
        return render(request, template_name, context={'server_name': server_name, 'services': server_services})


class Service_view(View):
    def get(self, request, server_name, service_name):
        try:
            service = Service.objects.filter(service_name=service_name)
        except:
            return redirect('/')
        server = Server.objects.filter(server_name=server_name)
        try:
            status_service = Status.objects.filter(service=service[0],server=server[0]).values_list("status", "version", "updated")
        except:
            return redirect('/')
        template_name = "service.html"
        return render(request, template_name, context={"status_service": status_service,
                                                       "service_name": service_name,
                                                       "server_name": server_name})


class Version_view(View):
    def get(self, request):
        statuses = Status.objects.all().exclude(service=99).order_by("server", "service", "-created").distinct("server", "service")
        labs = Lab.objects.all().exclude(pk=99)
        data_list = {}

        servers = Server.objects.all()
        for lab in labs:
            data_list[lab] = {}
            for server in servers:
                if server.lab == lab:
                    for s in statuses:
                        if s.version != "UNKNOWN":
                            if server.server_name == s.server.server_name:

                                if s.service.service_name not in data_list[lab]:
                                    data_list[lab][s.service.service_name] = []
                                if s.version not in data_list[lab][s.service.service_name]:
                                    data_list[lab][s.service.service_name].append(s.version)
        services_list = []
        for service_name in Service.objects.all().exclude(service_name="UNKNOWN"):
            services_list.append(service_name)

        template_name = "version.html"
        return render(request, template_name, context={'data': data_list,
                                                       'services': services_list,
                                                       'status': statuses})


class ServiceMoreDetail(View):
    def get(self, request, service_name):
        try:
            service = Service.objects.filter(service_name=service_name)[0]
        except:
            return redirect('/')
        q = Status.objects.filter(service=service).order_by("server", "service", "-created").distinct("server", "service").values_list("server__server_name", "service")
        server_list = []
        for server, service in q:
            server_list.append(server)

        template_name = "service_common.html"
        return render(request, template_name, context={"all_servers": server_list,
                                                       "service": service,
                                                       })


class Winnodes(View):

    @register.filter
    def get(self, request):
        q = {}

        for node in Winnode.objects.all().order_by("node_name"):
            q[node.node_name] = {}
            q[node.node_name]["vcenter"] = node.vcenter.vcenter_name
            q[node.node_name]["winenv"] = node.winenv.winenv_name
            q[node.node_name]["java_version"] = node.java_version
            q[node.node_name]["chrome_version"] = node.chrome_version
            q[node.node_name]["chromedriver_version"] = node.chromedriver_version
            q[node.node_name]["firefox_version"] = node.firefox_version
            q[node.node_name]["gecko_version"] = node.gecko_version
            q[node.node_name]["selenium_version"] = node.selenium_version
            q[node.node_name]["python_version"] = node.python_version
            q[node.node_name]["updated"] = {}
            q[node.node_name]["updated"]["date"] = node.updated
            if node.updated >= pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=10):
                q[node.node_name]["updated"]["status"] = 1
            elif node.updated < pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=10) and \
                    node.updated >= node.updated >= pytz.utc.localize(datetime.utcnow()) - timedelta(hours=3):
                q[node.node_name]["updated"]["status"] = 2
            elif node.updated < pytz.utc.localize(datetime.utcnow()) - timedelta(hours=3):
                q[node.node_name]["updated"]["status"] = 3

        template_name = 'winnode.html'
        return render(request, template_name, context={'winnodes': q})
