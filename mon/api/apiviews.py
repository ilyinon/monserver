from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from .models import Server, Service, Status, Winnode, winENV, vCenter, WindowsVersion
from .serializers import ServerSerializer, ServiceSerializer, StatusSerializer
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class ServerList(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class ServerDetail(generics.RetrieveDestroyAPIView):
    def get_queryset(self):
        queryset = Server.objects.filter(pk=self.kwargs['pk'])
        return queryset
    serializer_class = ServerSerializer


class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetail(generics.RetrieveDestroyAPIView):
    def get_queryset(self):
        queryset = Service.objects.filter(pk=self.kwargs['pk'])
        return queryset
    serializer_class = ServiceSerializer


class CreateStatus(generics.ListCreateAPIView):
    def get_queryset(self):
        q = Status.objects.all().order_by("server", "service", "-created").distinct("server", "service")
        return q

    serializer_class = StatusSerializer

    def post(self, request):
        s = Status()

        try:
            s.server = Server.objects.get(server_name=request.data.get("server"))
        except Server.DoesNotExist:
            s.server = Server.create(request.data.get("server"))

        try:
            s.service = Service.objects.get(service_name=request.data.get("service"))
        except Service.DoesNotExist:
            s.service = Service.create(request.data.get("service"))

        s.version = request.data.get("version")

        if request.data.get("status") == "True":
            s.status = True
        else:
            s.status = False
            logger.error("False status")

        prev_status = Status.objects.filter(server=s.server, service=s.service).last()
        if prev_status:
            if s.status == prev_status.status and s.version == prev_status.version:
                s = prev_status
                s.updated = timezone.now()
        logger.error(prev_status)
        try:
            s.save()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_201_CREATED)


class GetServiceStatus(generics.ListCreateAPIView):
    def get_queryset(self):
        server_id = Server.objects.filter(server_name=self.kwargs["server"]).values_list("pk")
        service_id = Service.objects.filter(service_name=self.kwargs["service"]).values_list("pk")
        q = Status.objects.filter(server_id=server_id[0], service_id=service_id[0]).order_by("-created")[:1]
        return q

    serializer_class = StatusSerializer


class CreateWinnodeStatus(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Winnode.objects.all()
        return queryset

    serializer_class = StatusSerializer

    def post(self, request):
        print(request.data)
        try:
            node = Winnode.objects.get(node_name=request.data.get("node_name"))
        except:
            node = Winnode()
            try:
                node.vcenter = vCenter.objects.get(vcenter_name="no_data")
            except:
                print("step 2 failed")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            node.node_name = request.data.get("node_name")

        try:
            node.winenv = winENV.objects.get(winenv_name=request.data.get("winenv"))
        except:
            print("step 3 failed")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("java_version"):
            node.java_version = request.data.get("java_version")
        if request.data.get("chrome_version"):
            node.chrome_version = request.data.get("chrome_version")
        if request.data.get("firefox_version"):
            node.firefox_version = request.data.get("firefox_version")
        if request.data.get("chromedriver_version"):
            node.chromedriver_version = request.data.get("chromedriver_version")
        if request.data.get("gecko_version"):
            node.gecko_version = request.data.get("gecko_version")
        if request.data.get("selenium_version"):
            node.selenium_version = request.data.get("selenium_version")
        if request.data.get("python_version"):
            node.python_version = request.data.get("python_version")
        if request.data.get("windows_activated"):
            node.windows_activated = request.data.get("windows_activated")
        if request.data.get("mac_address"):
            node.mac_address = request.data.get("mac_address")
        if request.data.get("ip_address"):
            node.ip_address = request.data.get("ip_address")
        if request.data.get("domain_name"):
            node.domain_name = request.data.get("domain_name")

        if request.data.get("windows_version"):
            try:
                node.windows_version = WindowsVersion.objects.get(windows_version=request.data.get("windows_version"))
            except:
                wv = WindowsVersion()
                wv.windows_version = request.data.get("windows_version")
                try:
                    wv.save()
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                node.windows_version = WindowsVersion.objects.get(windows_version=request.data.get("windows_version"))

        node.updated = timezone.now()
        print(node.java_version)
        node.save()

        try:
            node.save()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_201_CREATED)