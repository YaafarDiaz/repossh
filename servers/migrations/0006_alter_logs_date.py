# Generated by Django 4.2.13 on 2024-07-27 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0005_logs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='date',
            field=models.DateField(),
        ),
    ]
