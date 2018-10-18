from django.contrib import admin
from .models import Server, Service, Status, DC, Lab, Report

admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Status)
admin.site.register(DC)
admin.site.register(Lab)
admin.site.register(Report)
