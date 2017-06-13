# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View, TemplateView, DeleteView
from django.views.generic.edit import FormView, CreateView
# from django.views.generic.base import TemplateView

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User, Group

from .models import TimeClock, Store, Franchise, Employee, Manager, DaySchedule

from django.utils.safestring import mark_safe
from .controller import WeekCalendar

from .forms import UserForm

from datetime import date, datetime

from django.urls import reverse_lazy

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class HomeView(TemplateView):
    template_name = "DayPlanner/home.html"


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        user = self.request.user
        # manager = user.manager_set
        manager = Manager.objects.get(user = user)
        franchise = manager.franchise
        # Get count and the object of registered stores
        stores = franchise.store_set.all()
        storeCount = stores.count()
       
        # timeClockCount = 0
        # Get employee count given a franchise
        employeeCount  = 0
        timeClockCount = 0
        for store in stores:
            employeeCount += store.employee_set.all().count()
            timeClockCount += store.timeclock_set.all().count()

        context['employeeCount'] = employeeCount
        context['storeCount'] = storeCount
        context['timeClockCount'] = timeClockCount

        return context

    # def get(self,request):
    #     return HttpResponse("hello")

class RegisteredUsersView(FormView):
    template_name = "DayPlanner/registered_users.html"
    success_url = reverse_lazy("DayPlanner:registered_users")
    form_class = UserForm

    def form_valid(self, form):  
        context = super(RegisteredUsersView, self).form_valid(form)
        form.save()
        messages.success(self.request, 'User is succesfully created!')
        return context

    def form_invalid(self, form):
        context = super(RegisteredUsersView, self).form_invalid(form)
        for field in form:
            for error in field.errors:
                messages.error(self.request,error)
        return context
    
    def get_context_data(self, **kwargs):
        context = super(RegisteredUsersView, self).get_context_data(**kwargs)
        # groups = Group.objects.all()
        
        user = self.request.user
        franchise = Manager.objects.get(user = user).franchise

        # Backwar referencing of foriegn key in django
        managers = franchise.manager_set.all()
        stores = franchise.store_set.all()

        context['franchise'] = franchise
        context['managers'] = managers
        context['stores'] = stores

        return context

class DeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy("DayPlanner:registered_users")
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = kwargs["pk"])
        first_name = user.first_name
        last_name = user.last_name
        messages.success(request, first_name + " " + last_name + " is succesfully deleted!")
        return self.post(request, *args, **kwargs)

class CreateStoreView(View):
    success_url = reverse_lazy("DayPlanner:registered_users")
    def get(self, request, *args, **kwargs):
        
        user = request.user
        franchise = Manager.objects.get(user = user).franchise
        name = kwargs["store_name"]
        storeAddress = kwargs["store_address"]

        store = Store(franchise=franchise,name=name,address=storeAddress)
        if store:
            store.save()
            messages.success(request, store.name + " " + store.address + " is succesfully deleted!")
        else:
            messages.danger(request, "Something went Wrong!!")

        return HttpResponseRedirect(self.success_url)

class DeleteStoreView(DeleteView):
    model = Store
    success_url = reverse_lazy("DayPlanner:registered_users")
    def get(self, request, *args, **kwargs):
        print(kwargs["pk"])
        store = Store.objects.get(id = kwargs["pk"])
        messages.success(request, store.name + " " + " is succesfully deleted!")
        
        # print(store.employee_set)
        for employee in store.employee_set.all():
            user = employee.user
            first_name = user.first_name
            last_name = user.last_name
            messages.success(request, first_name + " " + last_name + " is deleted!")

        return self.post(request, *args, **kwargs)
 

class SchedulePlannerView(TemplateView):
    template_name = "DayPlanner/schedule_planner.html"

    def get_context_data(self, **kwargs):
        context = super(SchedulePlannerView, self).get_context_data(**kwargs)

        user = self.request.user
        franchise = Manager.objects.get(user = user).franchise
        stores = franchise.store_set.all()

        year = ""
        month = ""
        day = ""

        currentDate = datetime.now().date()

        argDate = None
        try:
            urlDate = kwargs["date"].split("-")
            year = int(urlDate[0])
            month = int(urlDate[1])
            day = int(urlDate[2])
            argDate = date(year,month,day)
        
        except KeyError:
            argDate = currentDate
      
        isBefore = False
        if argDate < currentDate:
            isBefore = True

        calendar = WeekCalendar(argDate)

        week = calendar.formatWeek()
        lastWeek = calendar.getPreviousWeek()
        nextWeek = calendar.getNextWeek()
        weekNumber = calendar.getWeekNumber()
        # lastWeek, week, nextWeek = calendar.formatweek(year,month,day)

        context['lastWeek'] = lastWeek
        context['nextWeek'] = nextWeek
        context['week'] = week
        context['isBefore'] = isBefore
        # context['stores'] = stores



        data = {}
        for store in stores:
            data[store] = {}
            for employee in store.employee_set.all():
                weekSchedule = []
                for day in week:
                    dayScedule = None
                    try:
                        dayScedule = employee.dayschedule_set.get(date=day[0])
                        # print dayScedule.startingTime
                        # print dayScedule.endTime
                    except ObjectDoesNotExist:
                        pass
                    weekSchedule.append(dayScedule)
    
                data[store][employee] = weekSchedule
        context['stores'] = data
        # print(data)
        return context


class TimeClockView(TemplateView):
    def get(self,request):
        return HttpResponse("Time Clock")