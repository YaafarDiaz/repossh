# Generated by Django 4.2.13 on 2024-07-06 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=20)),
                ('ip', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['ip'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('port', models.CharField(max_length=20)),
                ('log_path', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
