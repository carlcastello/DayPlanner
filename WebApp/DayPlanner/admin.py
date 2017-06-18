# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import TimeClock, Franchise, Manager, Store, Employee, DaySchedule, EmergencyContact
# Register your models here.
admin.site.register(EmergencyContact)
admin.site.register(Franchise)
admin.site.register(Manager)
admin.site.register(Store)
admin.site.register(Employee)
admin.site.register(TimeClock)

admin.site.register(DaySchedule)