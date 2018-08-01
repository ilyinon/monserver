from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from .models import Server, Service, Status
from .serializers import ServerSerializer, ServiceSerializer, StatusSerializer


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
        q = Status.objects.order_by("server").distinct("server", "service")

        queryset = q
        return queryset

    serializer_class = StatusSerializer

    def post(self, request):
        s = Status()
        server_id = request.data.get("server")
        s.server = Server.objects.get(pk=server_id)
        service_id = request.data.get("service")
        s.service = Service.objects.get(pk=service_id)
        if request.data.get("status"):
            s.status = True
        else:
            s.status = False
        try:
            s.save()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(request.data, status=status.HTTP_201_CREATED)
