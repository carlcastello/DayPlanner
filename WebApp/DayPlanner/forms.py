
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import TimeClock, Store, Franchise, Employee, Manager, Profile, EmergencyContact

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

        if self.cleaned_data["userType"] == "store":
            id = self.cleaned_data["typeID"]
            store = Store.objects.get(id = id)
            Employee.objects.create(
                user = user,
                store = store
            )
        elif self.cleaned_data["userType"] == "manager":
            id = self.cleaned_data["typeID"]
            franchise = Franchise.objects.get(id = id)
            Manager.objects.create(
                user = user,
                franchise = franchise
            )
        else:
            pass
            
class StoreForm(forms.ModelForm):
    name = forms.CharField(
        required = True,
        max_length = 100
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
            "location"
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

        firstName = self.cleaned_data["firstname"]
        if user.first_name != firstName and firstName != "":
            # print "Change Firstname"
            user.first_name = firstName
            
        lastName = self.cleaned_data["lastname"]
        if user.last_name != lastName and lastName != "":
            # print "Change Firstname"
            user.last_name = lastName

        email = self.cleaned_data["email"]
        if user.email != email and email != "":
            # print "Change Email"
            user.email = email

        address = self.cleaned_data["address"]
        if profile.address != address and address != "":
            # print "Change Address"
            profile.address = address

        cellNumber = self.cleaned_data["cellnumber"] 
        if profile.cellnumber != cellNumber and cellNumber != "":
            # print "Change Cell Phone"
            profile.cellnumber = cellNumber

        homeNumber = self.cleaned_data["homenumber"] 
        if profile.homenumber != homeNumber and homeNumber != "":
            # print "Change Cell Phone"
            profile.homenumber = homeNumber


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

        if commit:  

            contact.save()

        return contact