from django.contrib import admin
from .models import Server, Service, Status, DC, Lab, Report, vCenter, winENV, Winnode, Datastore, ESXiHost, WindowsVersion


class WinnodeAdmin(admin.ModelAdmin):
    list_display = ('node_name',)
    search_fields = ['node_name']

class vCenterAdmin(admin.ModelAdmin):
    list_display = ('vcenter_name',)

class winENVAdmin(admin.ModelAdmin):
    list_display = ('winenv_name',)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('server',)
    search_fields =['server']

admin.site.register(Server)
admin.site.register(Service)
admin.site.register(Status, StatusAdmin)
admin.site.register(DC)
admin.site.register(Lab)
admin.site.register(Report)
admin.site.register(vCenter, vCenterAdmin)
admin.site.register(winENV, winENVAdmin)
admin.site.register(Winnode, WinnodeAdmin)
admin.site.register(Datastore)
admin.site.register(ESXiHost)
admin.site.register(WindowsVersion)
