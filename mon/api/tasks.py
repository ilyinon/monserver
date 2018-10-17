from celery import shared_task
import os
import time
from .models import Server, Service, Status



@shared_task
def task_stop_server(server_id):
    pass