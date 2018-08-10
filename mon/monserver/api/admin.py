from django.contrib import admin
from .models import Server, Service, Status, DC

admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Status)
admin.site.register(DC)
