# Generated by Django 2.0.7 on 2018-11-26 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20181126_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='winnode',
            name='windows_activated',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]
