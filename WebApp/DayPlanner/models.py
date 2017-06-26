# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from uuid import uuid4

from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_delete

from django.utils.encoding import python_2_unicode_compatible
# import datetime

from django.utils import timezone

from simple_history.models import HistoricalRecords
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )

    address = models.CharField(
        max_length=100,
        blank=True
    )
    cellnumber = models.CharField(
        max_length=12,
        blank=True
    )
    homenumber = models.CharField(
        max_length=12,
        blank=True
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


    def delete(self, *args, **kwargs):
        self.user.delete()
        # return super(self.__class__, self).delete(*args, **kwargs)

class EmergencyContact(models.Model):
    firstname = models.CharField(
        max_length=100
    )
    lastname = models.CharField(
        max_length=100
    )
    cellnumber = models.CharField(
        max_length=12,
        blank=True
    )
    relationship = models.CharField(
        max_length=12,
        blank=True
    )
    homenumber = models.CharField(
        max_length=12,
        blank=True
    )
    profile = models.ForeignKey(
        Profile,
        on_delete = models.CASCADE
    )

class Franchise(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid4, 
        editable=False
    )
    name = models.CharField(        
        max_length=100
    )

    def __str__(self):              
        return self.name 

class Store(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid4, 
        editable=False
    )
    name = models.CharField(        
        max_length=100
    )
    location = models.CharField(
        max_length=100
    )
    number = models.PositiveIntegerField(

    )
    franchise = models.ForeignKey(
        Franchise, 
        on_delete=models.CASCADE
    )

    def __str__(self):              
        return self.name + " " + self.location
 
class Manager(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    franchise = models.ForeignKey(
        Franchise, 
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.profile.user.first_name + " " + self.profile.user.last_name


class Employee(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.profile.user.first_name + " " + self.profile.user.last_name




class Request(models.Model):
    date = models.DateTimeField(
        default=timezone.now
    )
    employee = models.OneToOneField(
        Employee,
        default=None,
        on_delete = models.CASCADE
    )
    content = models.TextField(
        default=None
    )


class TimeClock(models.Model):
    id = models.CharField(
        max_length=100, 
        unique=True, 
        default = uuid4,
        primary_key = True
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        default = None
    )
    signIn = models.DateTimeField()

    signOut = models.DateTimeField()

class DaySchedule(models.Model):
    id = models.CharField(
        max_length=100, 
        unique=True, 
        default = uuid4,
        primary_key = True
    )

    employee = models.ForeignKey(
        Employee
    )
    
    date = models.DateField()

    lastModified = models.DateTimeField(
        auto_now = True
    )
    
    startingTime = models.TimeField(
        default = None
    )
    endTime = models.TimeField(
        default = None
    )

    class Meta:
        unique_together = ("employee", "date")



@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user: # just in case user is not specified
        instance.user.delete()