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
        queryset = Status.objects.all()
        return queryset

    serializer_class = StatusSerializer

    def post(self, request):
        s = Status()
        s.server = request.data.get("server")
#        s.service = request.data.get("service")
        if request.data.get("status"):
            s.status = True
        else:
            s.status = False
        #s.status = request.data.get("status")
        s_status = s.save()

        if s_status:
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

