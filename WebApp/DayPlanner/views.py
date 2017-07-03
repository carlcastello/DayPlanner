# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, Http404, get_object_or_404

from django.contrib.auth.models import User

from .models import TimeClock, Store, Franchise, Employee, Manager, DaySchedule, Profile, EmergencyContact

from django.utils.safestring import mark_safe
from datetime import date, datetime

from django.utils import timezone

from .controller import WeekCalendar
from .forms import UserForm, StoreForm, UpdateProfile, EmergencyContactForm, UpdatEmergencyContactForm, RequestForm

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from easy_pdf.views import PDFTemplateView

decorators = [login_required,cache_control(no_cache=True, must_revalidate=True, no_store=True)]


# cache_control(no_cache=True, must_revalidate=True, no_store=True)
@method_decorator(decorators, name='dispatch')
class HomeView(TemplateView):
    template_name = None
    current_date = timezone.now().date()
    success_url = "DayPlanner:home"

    def get(self, *args, **kwargs):

        profile = self.request.user.profile
        # Render template depending on a user instance
        try:
            profile.manager
            self.template_name = "DayPlanner/home.html"
        except ObjectDoesNotExist:
            profile.employee
            self.template_name = "DayViewer/home.html"
        except:
            return HttpResponse(status=500)

        response = super(HomeView, self).get(*args, **kwargs)
        return response

    # Only the employees can post a request in Home View
    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        user = self.request.user
        employee = user.profile.employee

        user_request = employee.request


        if request.POST.get("submit"):
            # Create a Request for schedule

            form_arguments = {
                "datetime" : timezone.now(),
                "shifts" : request.POST.get("shifts"),
                "availability": request.POST.get("availability")
            }
            form = RequestForm(form_arguments,instance=user_request)
            if form.has_changed():
                if form.is_valid():
                    message = "Availability is updated."
                    self.form_valid(form,message)
                else:
                    self.form_invalid(form)

        else:
            raise Http404
        return redirect(self.success_url)

    def form_valid(self,form,message):
        form.save()
        messages.success(self.request, message)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request,field.label + ": " + error)
        return True

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        manager = None
        employee = None
        try:
            manager = self.request.user.profile.manager
        except ObjectDoesNotExist:
            employee = self.request.user.profile.employee
        except:
            return HttpResponse(status=500)

        # This method creates a different view between employee and manager
        if manager:
            context = self.__if_manager(manager,context)
        elif employee:
            context = self.__if_employee(employee,context,**kwargs)
        else:
            raise HttpResponse(status=500)

        return context

    def __if_manager(self,manager,context):

        franchise = manager.franchise
        # Get count and the object of registered stores
        stores = franchise.store_set.all()
        store_count = stores.count()

        # Get employee count given a franchise
        employee_count = 0
        time_clock_count = 0
        for store in stores:
            employees = store.employee_set.all()
	    employee_count += employees.count()
       	    for employee in employees:
		time_clock_count += employee.timeclock_set.all().count()

        context["isManager"] = True
        context['employeeCount'] = employee_count
        context['storeCount'] = store_count
        context['timeClockCount'] = time_clock_count

        return context

    def __if_employee(self,employee,context,**kwargs):
        # context["name"] = "Apple"

        date = self.__get_arg_date(kwargs)
        store = employee.store

        calendar = WeekCalendar(date)
        week = calendar.get_week()
        last_week = calendar.get_week_previous()
        next_week = calendar.get_week_next()

        user_request = None
        try:
            user_request = employee.request
        except ObjectDoesNotExist:
            pass

        context["user_request"] = user_request
        context["lastWeek"] = last_week
        context["nextWeek"] = next_week
        context["week"] = week
        context['stores'] = calendar.get_week_schedule([store])

        return context

    def __get_arg_date(self,kwargs):
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


# @cache_control(no_cache=True, must_revalidate=True)
@method_decorator(decorators, name='dispatch')
class ProfileView(TemplateView):
    template_name = "DayViewer/profile.html"

    def get(self, *args, **kwargs):

        # Limit this view for only employees
        try:
            self.request.user.profile.employee
        except ObjectDoesNotExist:
            raise Http404
        except:
            return HttpResponse(status=500)

        response = super(ProfileView, self).get(*args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = get_object_or_404(User,pk=kwargs["pk"])

        history = Profile.history.filter(user=user)
        profile = Profile.objects.get(user=user)

        context["profile"] = profile
        context["user_history"] = history
        return context


# @cache_control(no_cache=True, must_revalidate=True)
@method_decorator(decorators, name='dispatch')
class RegisteredUsersView(TemplateView):
    template_name = "DayPlanner/registered_users.html"
    success_url = "DayPlanner:registered_users"
    form_class = UserForm

    def get(self, *args, **kwargs):

        # Limit this view for only managers
        try:
            self.request.user.profile.manager
        except ObjectDoesNotExist:
            raise Http404
        except:
            return HttpResponse(status=500)

        response = super(RegisteredUsersView, self).get(*args, **kwargs)
        return response

    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        
        if request.POST.get("createUser"):
            form = UserForm(request.POST)
            if form.is_valid():
                string = request.POST.get("firstname") + " " + request.POST.get("lastname") + " has been created."
                # profile.changeReason = request.POST.get("first_name") + " - " + request.POST.get("last_name") + " " + "is created!"
                self.form_valid(form,string)
            else:
                self.form_invalid(form)

        elif request.POST.get("createStore"):
            franchise = Manager.objects.get(profile=request.user.profile).franchise.id

            form_arguments = {
                "name" : request.POST.get("name"),
                "location" : request.POST.get("location"),
                "franchise" : franchise,
                "number" : request.POST.get("number"),
            }
            form = StoreForm(form_arguments)
            if form.is_valid():
                string = request.POST.get("name") + " - " + request.POST.get("location") + " " + "is created!"
                self.form_valid(form,string)
            else:
                self.form_invalid(form)

        elif request.POST.get("deleteStore"):
            store = Store.objects.get(id = request.POST.get("storeid"))

            store_string = store.name + " - " + store.location + " " + " is deleted!"
            messages.success(request, store_string)

            for employee in store.employee_set.all():
                user = employee.user
                first_name = user.first_name
                last_name = user.last_name
                user_string = first_name + " " + last_name + " is deleted!"
                messages.success(request, user_string)
            store.delete()

        else:
            raise Http404("Form does not exist")
        return redirect(self.success_url)

    def form_valid(self,form,message):
        form.save()
        messages.success(self.request, message)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request,field.label + ": " + error)
        return True
    
    def get_context_data(self, **kwargs):
        context = super(RegisteredUsersView, self).get_context_data(**kwargs)
        
        user = self.request.user
        profile = Profile.objects.get(user=user)
        franchise = Manager.objects.get(profile=profile).franchise

        managers = franchise.manager_set.all()
        stores = franchise.store_set.all()
        context["isManager"] = True
        context['franchise'] = franchise
        context['managers'] = managers
        context['stores'] = stores

        return context


# @cache_control(no_cache=True, must_revalidate=True)
@method_decorator(decorators, name='dispatch')
class DetailUserView(TemplateView):
    template_name = "DayPlanner/detail_users.html"
    delete_url = "DayPlanner:registered_users"
    modify_url = "DayPlanner:user_detail_view"

    def get(self, *args, **kwargs):

        # Limit this view for only Managers
        try:
            self.request.user.profile.manager
        except ObjectDoesNotExist:
            raise Http404
        except:
            return HttpResponse(status=500)

        response = super(DetailUserView, self).get(*args, **kwargs)
        return response

    method_decorator(csrf_protect)
    def post(self,request,*args, **kwargs):
        user = User.objects.get(pk = kwargs["pk"])
        # profile = Profile.objects.get(user=user)
        profile = user.profile
        first_name = user.first_name
        last_name = user.last_name

        # print request.POST.get("confirm-user-delete")
        # Hahahahahahahhahahahahah
        # Refractor this please!!!
        if request.POST.get("deleteUser"):
            # account = None
            message = first_name + " " + last_name + " is deleted."

            self.profile_history(profile,message)
            profile.delete()

            messages.success(request, message)
            return redirect(self.delete_url)

        elif request.POST.get("modifyUser"):
            # print "Hello"
            form = UpdateProfile(request.POST, instance=profile)
            if form.has_changed():
                if form.is_valid():
                    message = first_name + " " + last_name + " has been modified."
                    self.form_valid(form,message)
                    # self.profile_history(profile, message)
                else:
                    self.form_invalid(form)

            return redirect(self.modify_url,user.pk)

        elif request.POST.get("createContact"):
            # print("Create Contact")
            form_arguments = {
                "firstname" : request.POST.get("firstname"),
                "lastname" : request.POST.get("lastname"),
                "relationship" : request.POST.get("relationship"),
                "homenumber" : request.POST.get("homenumber"),
                "cellnumber" : request.POST.get("cellnumber"),
                "profile" : profile.id
            }

            form = EmergencyContactForm(form_arguments)
            if form.is_valid():
                # form.save()
                message = request.POST.get("firstname") + " " + request.POST.get("lastname") + " is created as emergency contact."

                self.form_valid(form,message)
                self.profile_history(profile, message)
            else:
                self.form_invalid(form)
            return redirect(self.modify_url,user.pk)

        elif request.POST.get("editContact"):
            emergency_contact = EmergencyContact.objects.get(id=request.POST.get("contactidEdit"))
            form = UpdatEmergencyContactForm(request.POST, instance=emergency_contact)

            if form.has_changed():
                if form.is_valid():
                    message = request.POST.get("firstname") + " " + request.POST.get("lastname") + " is updated as emergency contact."
                    self.form_valid(form, message)
                    self.profile_history(profile, message)
                else:
                    self.form_invalid(form)

            return redirect(self.modify_url,user.pk)

        elif request.POST.get("deleteContact"):
            # print("Delete Contact")
            emergency_contact = EmergencyContact.objects.get(id=request.POST.get("contactidDelete"))
            
            message = emergency_contact.firstname + " " + emergency_contact.lastname + " is deleted as emergency contact."

            self.profile_history(profile, message)

            messages.success(self.request,message)
            
            emergency_contact.delete()
        
            return redirect(self.modify_url,user.pk)
            # pass

        raise Http404("Form does not exist")

    def profile_history(self,profile,string):
        profile.changeReason = string
        profile.save()

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

        history = Profile.history.filter(user=user)

        profile = user.profile
        context["isManager"] = True
        context["profile"] = profile
        context["user_history"] = history

        return context


# @cache_control(no_cache=True, must_revalidate=True)
@method_decorator(decorators, name='dispatch')
class SchedulePlannerView(TemplateView):
    template_name = "DayPlanner/schedule_planner.html"
    success_url = "DayPlanner:schedule_planner"
    pdf_url = "DayPlanner:schedule_pdf"

    current_date = timezone.now().date()

    def get(self, *args, **kwargs):

        # Limit this view for only managers
        try:
            self.request.user.profile.manager
        except ObjectDoesNotExist:
            raise Http404
        except:
            return HttpResponse(status=500)

        response = super(SchedulePlannerView, self).get(*args, **kwargs)
        return response

    method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if request.POST.get("export_to_pdf") is not None:
            store = request.POST.get("export_to_pdf")
            date = None
            try:
                date = kwargs["date"]
            except KeyError:
                date = str(self.current_date.year) + "-" + str(self.current_date.month) + "-" + str(self.current_date.day)

            return redirect(self.pdf_url,date,store)
        else:
            self.__handle_schedule(request)

        return redirect(self.success_url)

    def __handle_schedule(self,request):
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


    def get_context_data(self, **kwargs):
        context = super(SchedulePlannerView, self).get_context_data(**kwargs)

        franchise = self.request.user.profile.manager.franchise
        stores = franchise.store_set.all()

        date = self.__get_arg_date(kwargs)
        is_before = self.__get_is_before(date)

        calendar = WeekCalendar(date)
        week = calendar.get_week()
        last_week = calendar.get_week_previous()
        next_week = calendar.get_week_next()

        context["isManager"] = True
        context['lastWeek'] = last_week
        context['nextWeek'] = next_week
        context['week'] = week
        context['isBefore'] = is_before
        context['stores'] = calendar.get_week_schedule(stores)
        return context

    def __get_arg_date(self,kwargs):
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

    def __get_is_before(self,arg_date):
        if arg_date < self.current_date:
            return True
        return False

    # def get_week_schedule(self,stores,week):
    #     data = {}
    #     for store in stores:
    #         data[store] = {}
    #         for employee in store.employee_set.all():
    #             week_schedule = []
    #             for day in week:
    #                 day_scedule = {}
    #                 try:
    #                     day_scedule[day] = employee.dayschedule_set.get(date=day,employee=employee)
    #                 except ObjectDoesNotExist:
    #                     day_scedule[day] = None
    #                 week_schedule.append(day_scedule)
    #
    #             data[store][employee] = week_schedule
    #     return data


# @cache_control(no_cache=True, must_revalidate=True)
@method_decorator(decorators, name='dispatch')
class SchedulePDFView(PDFTemplateView):
    template_name = "EasyPDF/schedule.html"

    # download_filename = "hello.pdf"
    # pdf_filename =

    def get_context_data(self, **kwargs):
        context = super(SchedulePDFView, self).get_context_data(pagesize='A4',**kwargs)

        date = self.__get_arg_date(kwargs)
        store = Store.objects.get(id=kwargs["store"])

        calendar = WeekCalendar(date)

        context["store"] = store
        context["title"] = calendar.get_week_span()
        context["week"] = calendar.get_week()
        context["stores"] = calendar.get_week_schedule(stores = [store])

        return context


    def __get_arg_date(self,kwargs):
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


# @cache_control(no_cache=True, must_revalidate=True)
@method_decorator(decorators, name='dispatch')
class TimeClockView(TemplateView):
    template_name = "DayPlanner/time_clock.html"

    current_date = timezone.now().date()

    def get(self, *args, **kwargs):
        # Limit this view for only managers
        try:
            self.request.user.profile.manager
        except ObjectDoesNotExist:
            raise Http404
        except:
            return HttpResponse(status=500)

        response = super(TimeClockView, self).get(*args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super(TimeClockView, self).get_context_data(**kwargs)

        franchise = self.request.user.profile.manager.franchise
        stores = franchise.store_set.all()

        date = self.__get_arg_date(kwargs)
        is_before = self.__get_is_before(date)

        calendar = WeekCalendar(date)
        week = calendar.get_week()
        last_week = calendar.get_week_previous()
        next_week = calendar.get_week_next()

        context["isManager"] = True
        context['lastWeek'] = last_week
        context['nextWeek'] = next_week
        context['week'] = week
        context['isBefore'] = is_before
        context['stores'] = calendar.get_week_time_clock(stores)

        return context

    def __get_arg_date(self,kwargs):
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

    def __get_is_before(self,arg_date):
        if arg_date < self.current_date:
            return True
        return False

    # def get_week_schedule(self,stores,week):
    #     data = {}
    #     for store in stores:
    #         data[store] = {}
    #         for employee in store.employee_set.all():
    #             week_schedule = []
    #             for day in week:
    #                 day_scedule = {}
    #                 try:
    #                     day_scedule[day] = employee.dayschedule_set.get(date=day,employee=employee)
    #                 except ObjectDoesNotExist:
    #                     day_scedule[day] = None
    #                 week_schedule.append(day_scedule)
    #
    #             data[store][employee] = week_schedule
    #     return data
