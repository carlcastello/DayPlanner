
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

from .models import TimeClock, Store, Franchise, Employee, Manager

class UserForm(UserCreationForm):
    objectValue = forms.CharField(
        required = True,  
        max_length = 100
    )
    objectId = forms.CharField(
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
            "objectValue",
            "objectId",
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

        if self.cleaned_data["objectValue"] == "store":
            id = self.cleaned_data["objectId"]
            store = Store.objects.get(id = id)
            Employee.objects.create(
                user = user,
                store = store
            )
        elif self.cleaned_data["objectValue"] == "manager":
            id = self.cleaned_data["objectId"]
            franchise = Franchise.objects.get(id = id)
            Manager.objects.create(
                user = user,
                franchise = franchise
            )
        else:
            pass
            

    # def clean_username(self):
    #     pass
    # def clean(self):
    #     cleaned_data = super(UserForm, self).clean()
    # def clean_username(self, username):
    #     return username
        # try:
        #     User.objects.get(username__iexact=username)
        # except user_model.DoesNotExist:
        #     User.objects.get(username__iexact=username)

        # widgets = {
        #     'password1': forms.Textarea(
        #         attrs={
        #             "data-minlength":8
        #         }
        #     ),
        #     'password2': forms.Textarea(
        #         attrs={
        #             "data-match":"#inputPassword",
        #             "data-match-error":"Whoops, these don't match"
        #         }
        #     ),
        # }
