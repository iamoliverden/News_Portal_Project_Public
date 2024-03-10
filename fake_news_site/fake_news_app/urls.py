from django.urls import path
from .views import *



urlpatterns = [
    path('posts/', PostListView.as_view(), name='retriever_function'),
    path('posts/<str:id>', detail_function, name='detail_function'),
    path('posts/search/', SearchListView.as_view(), name='search_function'),
    path('posts/news/create/', create_post_function, name='create_post_function'),
    path('posts/articles/create/', create_post_function, name='create_post_function'),
    path('posts/<str:pk>/edit/', PostUpdate.as_view(), name='edit_post_function'),
    path('posts/<str:pk>/delete/', PostDelete.as_view(), name='delete_post_function'),
]