from django import forms
from .models import *


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'post_category', 'post_type']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.Select(choices=[(o.id, str(o.a_user)) for o in Author.objects.all()])
        self.fields['post_category'].widget = forms.SelectMultiple(choices=[(o.id, o.name.capitalize()) for o in Category.objects.all()])
        self.fields['post_type'].widget = forms.Select(choices=[('A', 'Article'), ('N', 'News')])

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