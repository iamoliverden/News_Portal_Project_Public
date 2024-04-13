from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import *
from django.views.generic.edit import *
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.mail import mail_managers
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_admins


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
        subject = "Hey Bro! Thanks for registration on Fake News App!"
        text = f"{user.username}, you have registered on Fake News successfully, so go dance jumpstyle!"
        html = (
            f'<b>{user.username}</b>, you have registered on '
            f'<a href="http://127.0.0.1:8000/fake_news_app/posts/">Fake News</a> successfully, so go dance jumpstyle!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        mail_managers(
            subject='New User Registration on Fake News App',
            message=f'User {user.username} has registered on Fake News App with email {user.email}!'
        )
        mail_admins(
            subject='New User Registration on Fake News App',
            message=f'User {user.username} has registered on Fake News App with email {user.email}!'
        )
        # save the user
        return user
