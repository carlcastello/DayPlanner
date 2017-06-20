# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.views.generic import TemplateView

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import User

from .models import TimeClock, Store, Franchise, Employee, Manager, DaySchedule, Profile, EmergencyContact

from django.utils.safestring import mark_safe
from datetime import date, datetime
from .controller import WeekCalendar
from .forms import UserForm, StoreForm, UpdateProfile, EmergencyContactForm, UpdatEmergencyContactForm

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from easy_pdf.views import PDFTemplateView

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
        store_count = stores.count()
       
        # timeClockCount = 0
        # Get employee count given a franchise
        employee_count  = 0
        time_clock_count = 0
        for store in stores:
            employee_count += store.employee_set.all().count()
            time_clock_count += store.timeclock_set.all().count()

        context['employeeCount'] = employee_count
        context['storeCount'] = store_count
        context['timeClockCount'] = time_clock_count

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

            form_arguments = {
                "name" : request.POST.get("name"),
                "location" : request.POST.get("location"),
                "franchise" : franchise
            }
            form = StoreForm(form_arguments)
            if form.is_valid():
                string = request.POST.get("name") + " - " + request.POST.get("location")
                self.form_valid(form,string)
            else:
                self.form_invalid(form)

        elif request.POST.get("deleteStore"):
            store = Store.objects.get(id = request.POST.get("storeid"))
        
            messages.success(request, store.name + " " + " is successfully deleted!")
 
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
            form_arguments = {
                "firstname" : request.POST.get("firstname"),
                "lastname" : request.POST.get("lastname"),
                "relationship" : request.POST.get("relationship"),
                "homenumber" : request.POST.get("homenumber"),
                "cellnumber" : request.POST.get("cellnumber"),
                "profile" : Profile.objects.get(user=user).id
            }

            form = EmergencyContactForm(form_arguments)
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
            emergency_contact = EmergencyContact.objects.get(id=request.POST.get("contactidEdit"))
            form = UpdatEmergencyContactForm(request.POST, instance=emergency_contact)
            if form.is_valid():
                message = request.POST.get("firstname") + " " + request.POST.get("lastname") + " is updated as emergency contact." 
                # messages.success(self.request,message)
                self.form_valid(form,message)
            else:
                pass

            return redirect(self.modify_url,user.pk)

        elif request.POST.get("deleteContact"):
            # print("Delete Contact")
            emergency_contact = EmergencyContact.objects.get(id=request.POST.get("contactidDelete"))
            
            message = emergency_contact.firstname + " " + emergency_contact.lastname + " is deleted as emergency contact."
            messages.success(self.request,message)
            
            emergency_contact.delete()
        
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
    pdf_url = "DayPlanner:schedule_pdf"

    current_date = datetime.now().date()

    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if request.POST.get("export_to_pdf"):
            # print "Hello"
            arg_date = None
            try:
                arg_date = kwargs["date"]
            except KeyError:
                arg_date = str(self.current_date.year) + "-" + str(self.current_date.month) + "-" + str(self.current_date.day)

            return redirect(self.pdf_url,arg_date)
        else:
            print "Boo"
            self.handle_schedule(request)
        return redirect(self.success_url)

    def handle_schedule(self,request):
        # Get input from post
        employee_id = request.POST.get("employee-id")
        employee = Employee.objects.get(id=employee_id)

        schedule_date = request.POST.get("schedule-date")

        starting_time = request.POST.get("from").encode("utf-8")
        end_time = request.POST.get("to").encode("utf-8")

        # SOLVED!!!!!!
        # Doesn't work if multiple post at the same date is created
        # Todo Fix when multiple post is created
        # Problem:
        # if two post are created with inputs that are a copy of each other,
        # both post will create a model that are exactly the same
        # try:
        schedule = DaySchedule.objects.filter(date=schedule_date, employee=employee)
        if not schedule:
            # print("Empty")
            if starting_time != "" and end_time != "":
                starting_time = datetime.strptime(starting_time, '%I:%M %p').time()
                end_time = datetime.strptime(end_time, '%I:%M %p').time()
                DaySchedule.objects.create(
                    employee=employee,
                    date=schedule_date,
                    startingTime=starting_time,
                    endTime=end_time,
                    lastModified=datetime.now()
                )
        else:
            # modify or delete
            # schedule = DaySchedule.objects.get(date = scheduleDate,employee = employee)
            # print(schedule.id)
            if starting_time != "" and end_time != "" and schedule:
                starting_time = datetime.strptime(starting_time, '%I:%M %p').time()
                end_time = datetime.strptime(end_time, '%I:%M %p').time()
                schedule.update(
                    startingTime=starting_time,
                    endTime=end_time,
                    lastModified=datetime.now()
                )
            else:
                schedule.delete()

    def handle_export(self,request):
        paragraphs = ["first paragraph", "second paragraph", "third paragraph"]
        html_string = render_to_string("DayPlanner/schedule.html", {"paragraphs": paragraphs})

        html = HTML(string=html_string)

        html.write_pdf(target="/tmp/mypdf.pdf");

        fs = FileSystemStorage("/tmp")
        with fs.open("mypdf.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename='mypdf.pdf'"
            return response

        return response

    def get_context_data(self, **kwargs):
        context = super(SchedulePlannerView, self).get_context_data(**kwargs)

        user = self.request.user
        franchise = Manager.objects.get(user = user).franchise
        stores = franchise.store_set.all()

        arg_date = self.get_arg_date(kwargs)
        is_before = self.get_is_before(arg_date)

        calendar = WeekCalendar(arg_date)
        week = calendar.formatWeek()
        last_week = calendar.getPreviousWeek()
        next_week = calendar.getNextWeek()

        context['lastWeek'] = last_week
        context['nextWeek'] = next_week
        context['week'] = week
        context['isBefore'] = is_before
        context['stores'] = self.get_week_schedule(stores,week)
        return context

    def get_arg_date(self,kwargs):
        arg_date = None
        try:
            urlDate = kwargs["date"].split("-")
            year = int(urlDate[0])
            month = int(urlDate[1])
            day = int(urlDate[2])
            arg_date = date(year, month, day)
        except KeyError:
            arg_date = self.current_date

        return arg_date

    def get_is_before(self,arg_date):
        if arg_date < self.current_date:
            return True
        return False

    def get_week_schedule(self,stores,week):
        data = {}
        for store in stores:
            data[store] = {}
            for employee in store.employee_set.all():
                week_schedule = []
                for day in week:
                    day_scedule = {}
                    try:
                        day_scedule[day] = employee.dayschedule_set.get(date=day,employee=employee)
                    except ObjectDoesNotExist:
                        day_scedule[day] = None
                    week_schedule.append(day_scedule)
    
                data[store][employee] = week_schedule
        return data

class SchedulePDFView(PDFTemplateView):
    template_name = "EasyPDF/schedule.html"

    # download_filename = "hello.pdf"
    # pdf_filename =

    def get_context_data(self, **kwargs):
        context = super(SchedulePDFView, self).get_context_data(pagesize='A4',**kwargs)

        return context

class TimeClockView(TemplateView):
    def get(self,request):
        return HttpResponse("Time Clock")