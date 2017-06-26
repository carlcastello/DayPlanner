# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import TimeClock, Franchise, Manager, Store, Employee, DaySchedule, EmergencyContact, Request, Profile
# Register your models here.
admin.site.register(EmergencyContact)
admin.site.register(Franchise)
admin.site.register(Manager)
admin.site.register(Store)
admin.site.register(Employee)
admin.site.register(TimeClock)
admin.site.register(Request)
admin.site.register(DaySchedule)
# admin.site.register(Profile)
admin.site.register(Profile,SimpleHistoryAdmin)
# admin.site.register(Profile,SimpleHistoryAdmin)

