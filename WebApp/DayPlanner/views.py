# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.views.generic import View, TemplateView, DeleteView
from django.views.generic.edit import FormView, CreateView
# from django.views.generic.base import TemplateView

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User, Group

from .models import TimeClock, Store, Franchise, Employee, Manager, DaySchedule, Profile, EmergencyContact

from django.utils.safestring import mark_safe
from .controller import WeekCalendar
from .forms import UserForm, StoreForm, UpdateProfile, EmergencyContactForm, UpdatEmergencyContactForm

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
    form_class = UserForm

    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        
        if request.POST.get("createUser"):
            form = UserForm(request.POST)
            if form.is_valid():
                string = request.POST.get("username")
                self.form_valid(form,string)
            else:
                self.form_invalid(form)

        elif request.POST.get("createStore"):
            franchise = Manager.objects.get(user = request.user).franchise.id

            formArguments = {
                "name" : request.POST.get("name"),
                "location" : request.POST.get("location"),
                "franchise" : franchise
            }
            form = StoreForm(formArguments)
            if form.is_valid():
                string = request.POST.get("name") + " - " + request.POST.get("location")
                self.form_valid(form,string)
            else:
                self.form_invalid(form)

        elif request.POST.get("deleteStore"):
            store = Store.objects.get(id = request.POST.get("storeid"))
        
            messages.success(request, store.name + " " + " is succesfully deleted!")
 
            for employee in store.employee_set.all():
                user = employee.user
                first_name = user.first_name
                last_name = user.last_name
                messages.success(request, first_name + " " + last_name + " is deleted!")
            store.delete()
        else:
            raise Http404("Form does not exist")
        return redirect(self.success_url)


    def form_valid(self,form,username):
        form.save()
        messages.success(self.request, username + " " +"is succesfully created!")

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request,field.label + ": " + error)
        return True
    
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
        # Hahahahahahahhahahahahah
        # Refractor this please!!!
        if request.POST.get("deleteUser"):
            # account = None
            
            first_name = user.first_name
            last_name = user.last_name
            
            profile = Profile.objects.get(user=user)
            profile.delete()

            messages.success(request, first_name + " " + last_name + " is deleted!")
            return redirect(self.delete_url)

        elif request.POST.get("modifyUser"):
            # print "Hello"
            form = UpdateProfile(request.POST, instance=user)
            if form.is_valid():
                message = "Successfully modified user profile"
                self.form_valid(form,message)
                # print "Valid"
            else:
                self.form_invalid(form)
                # print "Invalid"
            return redirect(self.modify_url,user.pk)

        elif request.POST.get("createContact"):
            # print("Create Contact")
            formArguments = {
                "firstname" : request.POST.get("firstname"),
                "lastname" : request.POST.get("lastname"),
                "relationship" : request.POST.get("relationship"),
                "homenumber" : request.POST.get("homenumber"),
                "cellnumber" : request.POST.get("cellnumber"),
                "profile" : Profile.objects.get(user=user).id
            }

            form = EmergencyContactForm(formArguments)
            if form.is_valid():
                # form.save()
                message = request.POST.get("firstname") + " " + request.POST.get("lastname") + " is created as emergency contact." 
                self.form_valid(form,message)
            else:
                self.form_invalid(form)
            return redirect(self.modify_url,user.pk)

        elif request.POST.get("editContact"):
            # print("Edit Contact")
            # print request.POST.get("contactidEdit")/
            emergencyContact = EmergencyContact.objects.get(id=request.POST.get("contactidEdit"))
            form = UpdatEmergencyContactForm(request.POST, instance=emergencyContact)
            if form.is_valid():
                message = request.POST.get("firstname") + " " + request.POST.get("lastname") + " is updated as emergency contact." 
                # messages.success(self.request,message)
                self.form_valid(form,message)
            else:
                pass

            return redirect(self.modify_url,user.pk)

        elif request.POST.get("deleteContact"):
            # print("Delete Contact")
            emergencyContact = EmergencyContact.objects.get(id=request.POST.get("contactidDelete"))
            
            message = emergencyContact.firstname + " " + emergencyContact.lastname + " is deleted as emergency contact."
            messages.success(self.request,message)
            
            emergencyContact.delete()
        
            return redirect(self.modify_url,user.pk)
            # pass

        raise Http404("Form does not exist")

    def form_valid(self,form,message):
        form.save()
        messages.success(self.request,message)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request,field.label + ": " + error)
        return True
    


    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)

        user = User.objects.get(pk = kwargs["pk"])
        # account = None

        profile = Profile.objects.get(user=user)
        
        context["profile"] = profile

        return context

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
        # try:
        schedule = DaySchedule.objects.filter(date = scheduleDate,employee = employee)
        if not schedule:
            # print("Empty")
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
        print(week)
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