
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import TimeClock, Store, Franchise, Employee, Manager

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
