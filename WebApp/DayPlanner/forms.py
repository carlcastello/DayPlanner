
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import TimeClock, Store, Franchise, Employee, Manager, Profile

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
        required = True
    )
    lastname = forms.CharField(
        required = True
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
        required = False
    )
    address = forms.CharField(
        required = False
    )
    homenumber = forms.CharField(
        required = False
    )
    cellnumber = forms.CharField(
        required = False
    )
    password = forms.CharField(
        required = False
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
        # pass
#     # class Meta:
#     #     model = User
#     #     fields = ('username', 'email', 'first_name', 'last_name')

#     # def clean_email(self):
#     #     username = self.cleaned_data.get('username')
#     #     email = self.cleaned_data.get('email')

#     #     if email and User.objects.filter(email=email).exclude(username=username).count():
#     #         raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#     #     return email

#     # def save(self, commit=True):
#     #     user = super(RegistrationForm, self).save(commit=False)
#     #     user.email = self.cleaned_data['email']

#     #     if commit:
#     #         user.save()

#     #     return user