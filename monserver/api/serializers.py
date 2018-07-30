from django.contrib.auth.models import User, Group
from .models import Server, Service, Status
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'server_name')

        def validate_server(self, value):
            qs = Server.objects.filter(server_name__iexact=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("The server must be unique")
            return value


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'service_name')



class StatusSerializer(serializers.ModelSerializer):
    server = serializers.SlugRelatedField(read_only=True, slug_field='server_name')
    service = serializers.SlugRelatedField(read_only=True, slug_field='service_name')

    class Meta:
        model = Status

        fields = ['server',
                  'service',
                  'status']


#        read_only_fields = ['server', 'service']

#    def create(self, validated_data):
##        server = Status.objects.create(**validated_data)
 #       service = Status.objects.create(**validated_data)
 #       status = Status.objects.create(**validated_data)
 #       return status

