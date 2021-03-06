from django.utils import timezone
from django.db import models
import re
import logging


logger = logging.getLogger(__name__)


class DC(models.Model):
    dc_name = models.CharField(max_length=50, blank=False, unique=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{} {}'.format(self.dc_name, self.pk)
        return template


class Lab(models.Model):
    lab_name = models.CharField(max_length=100, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lab_name


class Server(models.Model):
    server_name = models.CharField(max_length=100, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    dc = models.ForeignKey(DC, related_name='dc', on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, related_name='lab', on_delete=models.CASCADE)

    def __str__(self):
        template = '{}, domain = {}, lab = {}'.format(self.server_name, self.dc, self.lab)
        return template

    @classmethod
    def create(cls, new_name):
        domain = re.split('\.+', new_name)[1].upper()

        try:
            dc = DC.objects.get(dc_name=domain)
        except DC.DoesNotExist:
            dc = DC.objects.get(pk=99)

        logger.error(new_name)
        if re.search("^qa.+[a-zA-Z](01|03)[0-9].*\.", new_name):
            lab = Lab.objects.get(lab_name="QAUSLAB01")
        elif re.search("^qa.+[a-zA-Z](11|13)[0-9].*\.", new_name):
            lab = Lab.objects.get(lab_name="QAUSLAB02")
        elif re.search("^qa.+[a-zA-Z](61|63)[0-9].*\.", new_name):
            lab = Lab.objects.get(lab_name="TAGUSLAB03")
        elif re.search("^tag.+[a-zA-Z](01|03)[0-9].*\.", new_name):
            lab = Lab.objects.get(lab_name="TAGUSLAB04")
        elif re.search("^qa.+[a-zA-Z](81)[0-9].*\.", new_name):
            lab = Lab.objects.get(lab_name="TAGRULAB01")
        else:
            lab = Lab.objects.get(pk=99)

        new_server = cls(server_name=new_name, dc=dc, lab=lab)
        new_server.save()
        return new_server


class Service(models.Model):
    service_name = models.CharField(max_length=50, blank=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_name

    @classmethod
    def create(cls, new_name):
        new_service = cls(service_name=new_name)
        new_service.save()
        return new_service


class Status(models.Model):
    server = models.ForeignKey(Server, related_name='server',  on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='service', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{} {} {} {} {}'.format(self.created, self.status, self.server, self.service, self.updated)
        return template


class Report(models.Model):
    lab = models.ForeignKey(Lab, related_name='lab_report', on_delete=models.CASCADE)
    dc = models.ForeignKey(DC, related_name='dc_report', on_delete=models.CASCADE)
    server = models.ForeignKey(Server, related_name='server_report', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='service_report', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    status = models.CharField(max_length=20, default="No data")

    def __str__(self):
        template = '{} {} {} {} {}'.format(self.server, self.service, self.status, self.dc, self.lab)
        return template


class vCenter(models.Model):
    vcenter_name = models.CharField(max_length=50, blank=False, unique=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{} {}'.format(self.vcenter_name, self.pk)
        return template


class winENV(models.Model):
    winenv_name = models.CharField(max_length=50, blank=False, unique=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        template = '{} {}'.format(self.winenv_name, self.pk)
        return template

class Datastore(models.Model):
    datastore_name = models.CharField(max_length=100, blank=True, unique=True, default="0")

    def __str__(self):
        template = '{}'.format(self.datastore_name, self.pk)
        return template


class WindowsVersion(models.Model):
    windows_version = models.CharField(max_length=100, blank=True, unique=True, default="0")

    def __str__(self):
        template = '{}'.format(self.windows_version, self.pk)
        return template

class ESXiHost(models.Model):
    esxi_name = models.CharField(max_length=100, blank=True, unique=True, default="0")

    def __str__(self):
        template = '{}'.format(self.esxi_name, self.pk)
        return template

class Winnode(models.Model):
    node_name = models.CharField(max_length=50, blank=False, unique=True, default="", db_index=True)
    vcenter = models.ForeignKey(vCenter, related_name='vCenter',  on_delete=models.CASCADE, db_index=True)
    winenv = models.ForeignKey(winENV, related_name='winenv', on_delete=models.CASCADE, db_index=True)
    java_version = models.CharField(max_length=100, db_index=True)
    chrome_version = models.CharField(max_length=100, db_index=True)
    firefox_version = models.CharField(max_length=100, db_index=True)
    chromedriver_version = models.CharField(max_length=100, db_index=True)
    gecko_version = models.CharField(max_length=100, db_index=True)
    selenium_version = models.CharField(max_length=100, db_index=True)
    python_version = models.CharField(max_length=100, db_index=True)
    updated = models.DateTimeField(default=timezone.now, db_index=True)
    windows_activated = models.CharField(max_length=100, blank=True, db_index=True)
    mac_address = models.CharField(max_length=100, blank=True, db_index=True)
    ip_address = models.GenericIPAddressField(default="1.1.1.1")
    domain_name = models.CharField(max_length=100, blank=True, db_index=True)
    windows_version = models.ForeignKey(WindowsVersion, related_name='winver', default=1, on_delete=models.CASCADE, db_index=True)
    datastore_name = models.ForeignKey(Datastore, related_name='datastore', default=1, on_delete=models.CASCADE, db_index=True)
    esxi_host = models.ForeignKey(ESXiHost, related_name='esxi', default=1, on_delete=models.CASCADE, db_index=True)



    def __str__(self):
        template = '{} {} {}'.format(self.node_name, self.winenv, self.java_version)
        return template
