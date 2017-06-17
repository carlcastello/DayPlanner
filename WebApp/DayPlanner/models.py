# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from uuid import uuid4

from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_delete

from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )

    address = models.CharField(
        max_length=100
    )
    cellphone = models.CharField(
        max_length=12
    )
    homephone = models.CharField(
        max_length=12
    )

    def __str__(self):              
        return self.user.first_name + " " + self.user.last_name


    def delete(self, *args, **kwargs):
        self.user.delete()
        # return super(self.__class__, self).delete(*args, **kwargs)


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
    address = models.CharField(
        max_length=100
    )
    franchise = models.ForeignKey(
        Franchise, 
        on_delete=models.CASCADE
    )

    def __str__(self):              
        return self.name + " " + self.address
 
class Manager(Profile):
    franchise = models.ForeignKey(
        Franchise, 
        on_delete=models.CASCADE
    )

class Employee(Profile):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE
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