# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.views.generic import View, TemplateView, DeleteView
from django.views.generic.edit import FormView, CreateView
# from django.views.generic.base import TemplateView

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User, Group

from .models import TimeClock, Store, Franchise, Employee, Manager, DaySchedule, Profile

from django.utils.safestring import mark_safe
from .controller import WeekCalendar
from .forms import UserForm, ScheduleForm

from datetime import date, datetime

from django.urls import reverse_lazy

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404

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

class RegisteredUsersView(TemplateView):
    template_name = "DayPlanner/registered_users.html"
    success_url = "DayPlanner:registered_users"
    # form_class = UserForm

    # def form_valid(self, form):  
    #     context = super(RegisteredUsersView, self).form_valid(form)
    #     form.save()
    #     messages.success(self.request, 'User is succesfully created!')
    #     return context

    # def form_invalid(self, form):
    #     context = super(RegisteredUsersView, self).form_invalid(form)
    #     for field in form:
    #         for error in field.errors:
    #             messages.error(self.request,error)
    #     return context

    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        pass
    
    def get_context_data(self, **kwargs):
        context = super(RegisteredUsersView, self).get_context_data(**kwargs)
        
        user = self.request.user
        franchise = Manager.objects.get(user = user).franchise

        managers = franchise.manager_set.all()
        stores = franchise.store_set.all()

        context['franchise'] = franchise
        context['managers'] = managers
        context['stores'] = stores

        return context

class DetailUserView(TemplateView):
    template_name = "DayPlanner/detail_users.html"
    delete_url = "DayPlanner:registered_users"
    modify_url = "DayPlanner:user_detail_view"
   
    method_decorator(csrf_protect)
    def post(self,request,*args, **kwargs):
        user = User.objects.get(pk = kwargs["pk"])

        # print request.POST.get("confirm-user-delete")
        if request.POST.get("confirm-user-delete"):
            account = None
            
            first_name = user.first_name
            last_name = user.last_name
            
            profile = Profile.objects.get(user=user)
            profile.delete()

            messages.success(request, first_name + " " + last_name + " is succesfully deleted!")
            return redirect(self.delete_url)

        elif request.POST.get("modify-user-info"):
            return redirect(self.modify_url,user.pk)

        return Http404("Form does not exist")

    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)

        user = User.objects.get(pk = kwargs["pk"])
        # account = None

        profile = Profile.objects.get(user=user)
        
        context["profile"] = profile

        return context

class CreateStoreView(View):
    success_url = reverse_lazy("DayPlanner:registered_users")

    def post(self, request, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class DeleteStoreView(DeleteView):
    model = Store
    success_url = reverse_lazy("DayPlanner:registered_users")

    def get(self, request, *args, **kwargs):
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
    success_url = "DayPlanner:schedule_planner"

    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        # Get input from post
        employeeId = request.POST.get("employee-id")
        employee = Employee.objects.get(id=employeeId)
        
        scheduleDate = request.POST.get("schedule-date")

        startingTime = request.POST.get("from").encode("utf-8")
        endTime = request.POST.get("to").encode("utf-8")

        schedule = None

        # SOLVED!!!!!!
        # Doesn't work if multiple post at the same date is created 
        # Todo Fix when multiple post is created
        # Problem: 
        # if two post are created with inputs that are a copy of each other, 
        # both post will create a model that are exactly the same
        try:
            schedule = DaySchedule.objects.filter(date = scheduleDate,employee = employee)
        except ObjectDoesNotExist:
            if startingTime != "" and endTime != "":
                startingTime = datetime.strptime(startingTime, '%I:%M %p').time()
                endTime = datetime.strptime(endTime, '%I:%M %p').time()
                DaySchedule.objects.create(
                    employee = employee,
                    date = scheduleDate,
                    startingTime = startingTime,
                    endTime = endTime,
                    lastModified = datetime.now()
                )
        except Exception as e:
            raise e
        else:
            # modify or delete
            # schedule = DaySchedule.objects.get(date = scheduleDate,employee = employee)
            # print(schedule.id)
            if startingTime != "" and endTime != "" and schedule:
                startingTime = datetime.strptime(startingTime, '%I:%M %p').time()
                endTime = datetime.strptime(endTime, '%I:%M %p').time()
                schedule.update(
                    startingTime = startingTime,
                    endTime = endTime,
                    lastModified = datetime.now()
                )
            else:
                schedule.delete()
        
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(SchedulePlannerView, self).get_context_data(**kwargs)

        user = self.request.user
        franchise = Manager.objects.get(user = user).franchise
        stores = franchise.store_set.all()

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

        isPermitted = False
        if user not in franchise.manager_set.all():
            isPermitted = False


        calendar = WeekCalendar(argDate)
        week = calendar.formatWeek()
        lastWeek = calendar.getPreviousWeek()
        nextWeek = calendar.getNextWeek()
        # lastWeek, week, nextWeek = calendar.formatweek(year,month,day)

        context['lastWeek'] = lastWeek
        context['nextWeek'] = nextWeek
        context['week'] = week
        context['isBefore'] = isBefore
        # context['isPermitted'] = isPermitted
        context['stores'] = self.getWeekSchedule(stores,week)
        return context

    def getWeekSchedule(self,stores,week):
        data = {}
        for store in stores:
            data[store] = {}
            for employee in store.employee_set.all():
                weekSchedule = []
                for day in week:
                    dayScedule = {}
                    try:
                        dayScedule[day] = employee.dayschedule_set.get(date=day,employee=employee)
                    except ObjectDoesNotExist:
                        dayScedule[day] = None
                    weekSchedule.append(dayScedule)
    
                data[store][employee] = weekSchedule
        return data

class TimeClockView(TemplateView):
    def get(self,request):
        return HttpResponse("Time Clock")