
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from datetime import datetime
from simple_history.utils import update_change_reason
from .models import TimeClock, Store, Franchise, Employee, Manager, Profile, EmergencyContact, Request

class UserForm(UserCreationForm):
    userType = forms.CharField(
        required = True,  
        max_length = 100
    )
    typeID= forms.CharField(
        required = True, 
        max_length=100
    )
    firstname = forms.CharField(
        required = True,
        max_length=100
    )
    lastname = forms.CharField(
        required = True,
        max_length=100
    )
    email = forms.EmailField(
        required=False,
        max_length=100
    )
    address = forms.CharField(
        required=False,
        max_length=100
    )
    homenumber = forms.CharField(
        required=False,
        max_length=12
    )
    cellnumber = forms.CharField(
        required=False,
        max_length=12
    )
    class Meta:
        model = User
        fields = (
            "userType",
            "typeID",
            "username",
            "firstname",
            "lastname",
            "email",
            "address",
            "homenumber",
            "cellnumber",
            "password1", 
            "password2"
        )

    def save(self, commit = True):
        user = super(UserForm, self).save(commit = False)
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        profile = Profile.objects.create(
            user=user,
            address=self.cleaned_data["address"],
            homenumber=self.cleaned_data["homenumber"],
            cellnumber=self.cleaned_data["cellnumber"],
        )

        update_change_reason(profile, user.first_name + " " + user.last_name + " has been created.")

        if self.cleaned_data["userType"] == "store":
            id = self.cleaned_data["typeID"]
            store = Store.objects.get(id = id)
            print profile.user_id
            employee = Employee.objects.create(
                profile=profile,
                store = store
            )
            Request.objects.create(
                employee = employee
            )
        elif self.cleaned_data["userType"] == "manager":
            id = self.cleaned_data["typeID"]
            franchise = Franchise.objects.get(id = id)
            Manager.objects.create(
                profile=profile,
                franchise = franchise
            )
        else:
            pass

        return user
            
class StoreForm(forms.ModelForm):
    name = forms.CharField(
        required = True,
        max_length = 100
    )
    number = forms.IntegerField(
        required = True,
    )
    location = forms.CharField(
        required = True,
        max_length = 100
    )
    class Meta:
        model = Store
        fields = (
            "franchise",
            "name",
            "location",
            "number"
        )

class UpdateProfile(forms.ModelForm):
    username = forms.CharField()
    firstname = forms.CharField()
    lastname = forms.CharField()
    email = forms.EmailField(
        required = False,
        max_length=100
    )
    address = forms.CharField(
        required = False,
        max_length=100
    )
    homenumber = forms.CharField(
        required = False,
        max_length=12
    )
    cellnumber = forms.CharField(
        required = False,
        max_length=12
    )
    password = forms.CharField(
        required = False,
    )
    
    class Meta:
        model = User
        fields = (
            "username",
            "firstname",
            "lastname",
            "email",
            "address",
            "homenumber",
            "cellnumber",
            # "password"
        )


    def clean_username(self):
        username = self.cleaned_data.get("username")
        if self.instance.user.username == username:
            return username

        if User.objects.filter(username=username).exclude(username=self.instance).count() > 0:
            raise forms.ValidationError("Username is already in use.")

        return username


    def save(self, commit = True):
        profile = self.instance
        user = profile.user

        first_name = user.first_name
        last_name = user.last_name

        print self.cleaned_data
        user.username = self.clean_username()
        user.first_name = self.cleaned_data["firstname"]
        # print self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]

        if commit:
            # user.password = user.password
            user.save()
            profile.changeReason = first_name + " " + last_name + " has been modified."
            profile.save()
            return user

        # return False

class EmergencyContactForm(forms.ModelForm):
    firstname = forms.CharField(
        max_length = 100,
        required = True
    )
    lastname = forms.CharField(
        max_length = 100,
        required = True
    )
    relationship = forms.CharField(
        max_length = 100,
        required = True
    )
    homenumber = forms.CharField(
        required = False,
        max_length=12
    )
    cellnumber = forms.CharField(
        required = False,
        max_length=12
    )
    class Meta:
        model = EmergencyContact
        fields = (
            "profile" ,
            "firstname",
            "lastname",
            "relationship",
            "homenumber",
            "cellnumber",
        )

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            "availability",
            "shifts",
            "datetime"
        )

class UpdatEmergencyContactForm(forms.ModelForm):
    firstname = forms.CharField(
        max_length = 100,
        required = True
    )
    lastname = forms.CharField(
        max_length = 100,
        required = True
    )
    relationship = forms.CharField(
        max_length = 100,
        required = True
    )
    homenumber = forms.CharField(
        required = False,
        max_length=12
    )
    cellnumber = forms.CharField(
        required = False,
        max_length=12
    )

    class Meta:
        model = EmergencyContact
        fields = (
            "firstname",
            "lastname",
            "relationship",
            "homenumber",
            "cellnumber",
        )
