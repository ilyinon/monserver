# Generated by Django 2.0.7 on 2018-08-14 16:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180814_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='status',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]