# Generated by Django 2.0.7 on 2018-11-28 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_winnode_windows_activated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datastore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datastore_name', models.CharField(blank=True, default='0', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ESXiHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esxi_name', models.CharField(blank=True, default='0', max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WindowsVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('windows_version', models.CharField(blank=True, default='0', max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='winnode',
            name='domain_name',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AddField(
            model_name='winnode',
            name='ip_address',
            field=models.GenericIPAddressField(default='1.1.1.1'),
        ),
        migrations.AddField(
            model_name='winnode',
            name='mac_address',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AddField(
            model_name='winnode',
            name='datastore_name',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='datastore', to='api.Datastore'),
        ),
        migrations.AddField(
            model_name='winnode',
            name='esxi_host',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='esxi', to='api.ESXiHost'),
        ),
        migrations.AddField(
            model_name='winnode',
            name='windows_version',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='winver', to='api.WindowsVersion'),
        ),
    ]
