from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.views.generic.edit import *
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        # by default, we create common users, authors will need to contact managers to be added to the author's group
        admin = Group.objects.get(name="common_users")
        user.groups.add(admin)
        return user
