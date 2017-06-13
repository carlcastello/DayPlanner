# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 06:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DaySchedule',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Franchise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DayPlanner.Franchise')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DayPlanner.Franchise')),
            ],
        ),
        migrations.CreateModel(
            name='TimeClock',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('signIn', models.DateTimeField()),
                ('signOut', models.DateTimeField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DayPlanner.Employee')),
                ('store', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='DayPlanner.Store')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DayPlanner.Store'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dayschedule',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DayPlanner.Employee'),
        ),
    ]