# Generated by Django 2.0.7 on 2018-10-18 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='dc',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='dc_report', to='api.DC'),
            preserve_default=False,
        ),
    ]
