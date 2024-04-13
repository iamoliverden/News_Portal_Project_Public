from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import *
from .filters import *
from .forms import *
from .models import *
from django.contrib.auth.mixins import *
from django.contrib.auth.models import *
from django.views.generic.edit import *
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Count


class PostListView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'app_response'
    ordering = ['-created_at']
    paginate_by = 10

    # create search_function
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # create context that will be passed to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class SearchListView(PostListView):
    template_name = 'search.html'


# create detail_function
def detail_function(request, id):
    news_post = Post.objects.get(id=id)
    return render(request, 'news_post.html', context={'post': news_post})


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    login_url = '/accounts/login/'
    permission_required = 'fake_news_app.add_post'
    raise_exception = True
    template_name = 'create_article.html'
    form_class = PostForm
    success_url = reverse_lazy('retriever_function')

    def form_valid(self, form):
        if form.instance.post_type == "N":
            self.template_name = 'create_news.html'
        return super().form_valid(form)


# create post update class
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('fake_news_app.change_post',)
    raise_exception = True
    form_class = EditForm
    model = Post
    template_name = 'edit_post.html'


# create post delete class
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('fake_news_app.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('retriever_function')


class CategoryListView(ListView):  # shows all available cats and the num of posts in each cat
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories_list'
    ordering = ['name']
    paginate_by = 10


@login_required(login_url='/accounts/login/')  # subscribe to the category
def subscribe_function(request, pk):
    _user = request.user
    _category = get_object_or_404(Category, id=pk)  # Use get_object_or_404 to handle non-existent categories

    # Check if the user is already a subscriber of the category
    if not Subscriber.objects.filter(subscriber=_user, categories=_category).exists():
        # Create a Subscriber instance if it doesn't exist
        subscriber, created = Subscriber.objects.get_or_create(subscriber=_user)
        # Add the category to the subscriber's categories
        subscriber.categories.add(_category)
        message = f'You have subscribed to the category {_category.name.upper()}'
    else:
        message = f'You are already subscribed to the category {_category.name.upper()}'

    return render(request, 'subscribe.html', context={'category': _category, 'message': message})

@login_required(login_url='/accounts/login/')  # unsubscribe from the category
def unsubscribe_function(request, pk):
    _user = request.user
    _category = get_object_or_404(Category, id=pk)  # Use get_object_or_404 to handle non-existent categories

    # Check if the user is already a subscriber of the category
    subscriber = Subscriber.objects.filter(subscriber=_user, categories=_category)
    if subscriber.exists():
        # Remove the category from the subscriber's categories
        subscriber.first().categories.remove(_category)
        message = f'You have unsubscribed from the category {_category.name.upper()}.'
    else:
        message = f'You are not subscribed to the category {_category.name.upper()}.'

    return render(request, 'subscribe.html', context={'category': _category, 'message': message})


class PostListViewByCategory(PostListView):  # allows you to view posts by category
    template_name = 'posts_by_category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.category_id = self.kwargs.get('category_id')
        if self.category_id:
            queryset = queryset.filter(post_category__id=self.category_id)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(id=self.category_id)
        return context


class UserCategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'subscriptions.html'
    context_object_name = 'categories_list'
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(subscriber__subscriber=user)