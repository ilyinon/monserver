from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from .models import Server, Service, Status
from .serializers import ServerSerializer, ServiceSerializer, StatusSerializer
import logging

logger = logging.getLogger(__name__)

class ServerList(generics.ListCreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

#(generics.RetrieveDestroyAPIView)
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
        #q = Status.objects.all().order_by("created").distinct("server", "service")

        queryset = q
        return queryset

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

    def post(self, request, server, service):
        s = Status()
        s.server = Server.objects.get(server_name=server)

        s.service = Service.objects.get(service_name=service)
        s.version = request.data.get("version")

        if request.data.get("status") == "True":
            s.status = True


        else:
            s.status = False
            logger.error("False status")
        try:
            s.save()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_201_CREATED)
