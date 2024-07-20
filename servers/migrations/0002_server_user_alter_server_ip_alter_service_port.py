# Generated by Django 4.2.13 on 2024-07-19 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='user',
            field=models.CharField(default='user', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='server',
            name='ip',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='service',
            name='port',
            field=models.IntegerField(),
        ),
    ]