from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFromToRangeFilter, NumberFilter, DateFilter
from .models import Post
import datetime
from django import forms

class PostFilter(FilterSet):
    author__a_user__username = CharFilter(field_name='author__a_user__username', lookup_expr='icontains',
                                          label='Author', widget=forms.TextInput(attrs={'placeholder': 'Tov.Stalin'}))
    post_type = ChoiceFilter(choices=[('A', 'Article'), ('N', 'News')], label='Post Type')
    created_at = DateFilter(field_name='created_at', lookup_expr='gte', label='Date (From)', widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})) # NumberFilter(method='filter_by_year', label='Year', widget=forms.TextInput(attrs={'placeholder': '2024'}))
    post_category__name = CharFilter(field_name='post_category__name', lookup_expr='icontains', label='Category', widget=forms.TextInput(attrs={'placeholder': 'Trump'}))
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Title', widget=forms.TextInput(attrs={'placeholder': 'The Title Contains...'}))

    class Meta:
        model = Post
        fields = ['author__a_user__username', 'post_type', 'created_at', 'post_category__name', 'title']
