# Generated by Django 3.1.7 on 2021-03-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0003_remove_route_distance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
