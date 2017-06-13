# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DayPlanner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayschedule',
            name='endTime',
            field=models.TimeField(default=None),
        ),
        migrations.AddField(
            model_name='dayschedule',
            name='lastModified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='dayschedule',
            name='startingTime',
            field=models.TimeField(default=None),
        ),
        migrations.AlterField(
            model_name='dayschedule',
            name='date',
            field=models.DateField(),
        ),
    ]