# Generated by Django 4.2.13 on 2024-07-23 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0002_server_user_alter_server_ip_alter_service_port'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='server',
            options={'ordering': ['id']},
        ),
    ]
