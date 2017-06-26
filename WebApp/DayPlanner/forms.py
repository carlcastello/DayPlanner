
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from simple_history.utils import update_change_reason

from datetime import datetime

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
    class Meta:
        model = User
        fields = (
            "userType",
            "typeID",
            "username",
            "firstname",
            "lastname",
            "password1", 
            "password2"
        )

    def save(self, commit = True):
        user = super(UserForm, self).save(commit = False)
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]


        if commit:
            user.save()

        profile = Profile.objects.create(
            user=user
        )
        update_change_reason(profile, "User is created.")

        # print profile.user.id,"======================="

        if self.cleaned_data["userType"] == "store":
            id = self.cleaned_data["typeID"]
            store = Store.objects.get(id = id)
            print profile.user_id
            Employee.objects.create(
                profile=profile,
                store = store
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
        if User.objects.filter(username=username).exclude(username=self.instance).count() > 0:
            raise forms.ValidationError("Username is already in use.")
        return username

    def save(self, commit = True):
        user = self.instance
        # password = user.password
        # print password
        # user.password = user.password
        profile = Profile.objects.get(user = user)
        # Prevents empty input
        userName = self.cleaned_data["username"]
        if user.username != userName and userName != "":
            # print "Username Change"
            user.username = userName
            # reason += "Username is changed from " + user.username + " to " + userName + "."

        firstName = self.cleaned_data["firstname"]
        if user.first_name != firstName and firstName != "":
            # print "Change Firstname"
            user.first_name = firstName
            # reason += "Username is changed from " + user.username + " to " + userName + "."
            
        lastName = self.cleaned_data["lastname"]
        if user.last_name != lastName and lastName != "":
            # print "Change Firstname"
            user.last_name = lastName
            # reason += "Username is changed from " + user.username + " to " + userName + "."

        email = self.cleaned_data["email"]
        if user.email != email and email != "":
            # print "Change Email"
            user.email = email
            # reason += "Username is changed from " + user.username + " to " + userName + "."

        address = self.cleaned_data["address"]
        if profile.address != address and address != "":
            # print "Change Address"
            profile.address = address
            # reason += "Username is changed from " + user.username + " to " + userName + "."

        cellNumber = self.cleaned_data["cellnumber"] 
        if profile.cellnumber != cellNumber and cellNumber != "":
            # print "Change Cell Phone"
            profile.cellnumber = cellNumber
            # reason += "Username is changed from " + user.username + " to " + userName + "."

        homeNumber = self.cleaned_data["homenumber"] 
        if profile.homenumber != homeNumber and homeNumber != "":
            # print "Change Cell Phone"
            profile.homenumber = homeNumber
        # reason += "Username is changed from " + user.username + " to " + userName + "."

        # do custom stuff
        # profile.changeReason = "User information is modified."
        # profile._history_date = datetime.now()

        if commit:
            user.password = user.password
            user.save()
            profile.save()

        return user

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

    def save(self, commit=True):
        user = super(EmergencyContactForm, self).save(commit=False)

        # profile = self.cleaned_data["profile"]
        # profile.changeReason = "An emergency contact is created."
        # profile.save()

        if commit:
            user.save()
        return user

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            "employee",
            "content"
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

    def save(self, commit = True):
        contact = self.instance

        firstName = self.cleaned_data["firstname"]
        if contact.firstname != firstName and firstName != "":
            # print "Change Firstname"
            contact.firstname = firstName
            
        lastName = self.cleaned_data["lastname"]
        if contact.lastname != lastName and lastName != "":
            # print "Change Firstname"
            contact.lastname = lastName
        
        relationship = self.cleaned_data["relationship"] 
        if contact.relationship != relationship and relationship != "":
            # print "Change relationship"
            contact.relationship = relationship

        cellNumber = self.cleaned_data["cellnumber"] 
        if contact.cellnumber != cellNumber and cellNumber != "":
            # print "Change Cell Phone"
            contact.cellnumber = cellNumber

        homeNumber = self.cleaned_data["homenumber"] 
        if contact.homenumber != homeNumber and homeNumber != "":
            # print "Change Cell Phone"
            contact.homenumber = homeNumber

        # profile = Profile.objects.get(self.cleaned_data["profile"])
        # profile.changeReason = "An emergency contact is created."

        if commit:
            contact.save()
        return contact