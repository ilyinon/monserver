from django.db import models


class Server(models.Model):
    server_name = models.CharField(max_length=100, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.server_name


class Service(models.Model):
    service_name = models.CharField(max_length=50, unique=True)
    version = models.CharField(max_length=50)

    def __str__(self):
        return self.service_name


class Status(models.Model):
    server = models.ForeignKey(Server, related_name='server',  on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='service', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created, self.status

#    class Meta:
#        unique_together = ("server", "service")

    def last_status(self):
        """Get last status for whole server and services"""
        queryset = Status.objects.all()
        return queryset
