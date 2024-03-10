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


class PostListView(ListView):
    model = Post
    template_name = 'news.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'app_response'
    ordering = ['-created_at']
    paginate_by = 10

    # create search_function
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

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


# create post function:
@login_required(login_url='/accounts/login/')
@permission_required('fake_news_app.add_post', raise_exception=True)
def create_post_function(request):
    form = PostForm()
    indicator = ""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post_instance = form.save(commit=False)
            post_instance.post_type = form.cleaned_data['post_type'].upper()
            indicator = post_instance.post_type
            category_name = form.cleaned_data['post_category'].lower()

            post_instance.save()

            if Category.objects.filter(name=category_name).exists():
                category_id = Category.objects.get(name=category_name).id
                post_instance.post_category.add(category_id)

            else:
                new_category = Category.objects.create(name=category_name)
                category_id = new_category.id
                post_instance.post_category.add(category_id)

            return HttpResponseRedirect('/fake_news_app/posts/')

    if indicator == "N":
        return render(request, 'create_news.html', context={'form': form})
    else:
        return render(request, 'create_article.html', context={'form': form})


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


