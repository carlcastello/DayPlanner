# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 06:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DayPlanner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeclock',
            name='store',
        ),
        migrations.AddField(
            model_name='timeclock',
            name='date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='dayschedule',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
