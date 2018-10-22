from celery.decorators import periodic_task
from .models import Server, Status, Report, Service, DC, Lab
import pytz

from datetime import datetime, timedelta


@periodic_task(run_every=timedelta(seconds=10))
def every_10_seconds():
        servers = Server.objects.all()
        status = Status.objects.all().exclude(service=99).order_by("server", "service", "-created").distinct("server", "service")
        time_threshold = pytz.utc.localize(datetime.utcnow()) - timedelta(minutes=3)
        status_list = {}
        for qstatus in status:
            status_list[qstatus.server.server_name] = {}
            status_list[qstatus.server.server_name]["service"] = qstatus.service.service_name
            status_list[qstatus.server.server_name]["version"] = qstatus.version
            status_list[qstatus.server.server_name]["status"] = qstatus.status
            status_list[qstatus.server.server_name]["created"] = qstatus.created
            status_list[qstatus.server.server_name]["updated"] = qstatus.updated

        for server in servers:
            if Report.objects.filter(server=server).exists():
                report = Report.objects.get(server=server)
            else:
                report = Report()
                report.server = Server.objects.get(server_name=server.server_name)

            report.dc = server.dc
            report.lab = server.lab
            if server.server_name in status_list:
                report.service = Service.objects.get(service_name=status_list[server.server_name]["service"])
                report.created = status_list[server.server_name]["created"]
                report.updated = status_list[server.server_name]["updated"]
                if report.updated < time_threshold or not report.status:
                    report.status = False
                else:
                    report.status = True
                report.version = status_list[server.server_name]["version"]
            else:
                report.service = Service.objects.get(service_name="UNKNOWN")
                report.created = "2001-10-10"
                report.updated = "2001-10-10"
                report.status = False
            report.save()
