from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('posts/', cache_page(5)(PostListView.as_view()), name='retriever_function'),
    path('posts/<str:pk>', detail_function, name='detail_function'),
    path('posts/search/', SearchListView.as_view(), name='search_function'),
    path('posts/news/create/', PostCreateView.as_view(), name='create_post_function'),
    path('posts/articles/create/', PostCreateView.as_view(), name='create_post_function'),
    path('posts/<str:pk>/edit/', PostUpdate.as_view(), name='edit_post_function'),
    path('posts/<str:pk>/delete/', PostDelete.as_view(), name='delete_post_function'),
    path('categories/', CategoryListView.as_view(), name='categories_function'),
    path('categories/<int:pk>/subscribe/', subscribe_function, name='subscribe_function'),
    path('categories/<int:pk>/unsubscribe/', unsubscribe_function, name='unsubscribe_function'),
    path('posts/category/<int:category_id>/', PostListViewByCategory.as_view(), name='posts_by_category'),
    path('subscriptions/', UserCategoryListView.as_view(), name='show_subscriptions_function'),
    path('test_logging/', test_logging, name='test_logging'),
]
