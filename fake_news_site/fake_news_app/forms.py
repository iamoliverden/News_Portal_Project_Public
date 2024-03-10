from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    post_category = forms.CharField(max_length=200, required=True, help_text='Enter a category (one word) for the post')
    post_type = forms.CharField(max_length=16, required=True, help_text='Enter "A" for an article or "N" for news')

    class Meta:
        model = Post
        fields = ['author', 'title', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.Select(choices=[(o.id, str(o.a_user)) for o in Author.objects.all()])

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        post_category = cleaned_data.get('post_category')
        post_type = cleaned_data.get('post_type')
        if title == content:
            raise forms.ValidationError('Title and content must be different')
        if content is None:
            raise forms.ValidationError('Content must not be empty')
        if title is None:
            raise forms.ValidationError('Title must not be empty')
        if post_category is None:  # Validate 'post_category'
            raise forms.ValidationError('Post category must not be empty')
        if post_type.upper() not in ['A', 'N']:  # Validate 'post_type'
            raise forms.ValidationError('Post type must be "A" or "N"')

        return cleaned_data


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type', 'post_category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        if title == content:
            raise forms.ValidationError('Title and content must be different')
        if content is None:
            raise forms.ValidationError('Content must not be empty')
        if title is None:
            raise forms.ValidationError('Title must not be empty')

        return cleaned_data


