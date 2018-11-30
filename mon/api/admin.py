from django.contrib import admin
from .models import Server, Service, Status, DC, Lab, Report, vCenter, winENV, Winnode, Datastore, ESXiHost, WindowsVersion

admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Status)
admin.site.register(DC)
admin.site.register(Lab)
admin.site.register(Report)
admin.site.register(vCenter)
admin.site.register(winENV)
admin.site.register(Winnode)
admin.site.register(Datastore)
admin.site.register(ESXiHost)
admin.site.register(WindowsVersion)
