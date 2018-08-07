from django.db import models


class DC(models.Model):
    dc_name = models.CharField(max_length=50, blank=False, unique=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{} {}'.format(self.dc_name, self.pk)
        return template


class Server(models.Model):
    server_name = models.CharField(max_length=100, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    dc = models.ForeignKey(DC, related_name='dc', on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.server_name


class Service(models.Model):
    service_name = models.CharField(max_length=50, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_name


class Status(models.Model):
    server = models.ForeignKey(Server, related_name='server',  on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='service', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{} {} {}'.format(self.created, self.status, self.server, self.service)
        return template

