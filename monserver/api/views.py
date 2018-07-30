from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Server, Service, Status
from monserver.api.serializers import UserSerializer, GroupSerializer, ServerSerializer, ServiceSerializer, StatusSerializer



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

class SentStatus(APIView):
    def post(self, request, pk, choice_pk):
        status_by = request.data.get("status_by")
