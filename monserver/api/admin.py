from django.contrib import admin
from .models import Server, Service, Status

admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Status)
