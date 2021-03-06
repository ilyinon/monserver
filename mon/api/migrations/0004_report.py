# Generated by Django 2.0.7 on 2018-10-18 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180814_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('status', models.CharField(default='No data', max_length=20)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_report', to='api.Lab')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='server_report', to='api.Server')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_report', to='api.Service')),
            ],
        ),
    ]
