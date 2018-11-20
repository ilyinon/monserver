# Generated by Django 2.0.7 on 2018-08-14 14:30

from django.db import migrations
from django.core.management import call_command


def loadfixture(apps, schema_editor):
    call_command('loaddata', 'winnode_data.json')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_vcenter_winenv_winnode'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]
