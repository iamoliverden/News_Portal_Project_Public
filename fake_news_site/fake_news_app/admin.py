from django.contrib import admin
from .models import Author, Category, Post, PostCategory
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    model = Post

class CategoryAdmin(TranslationAdmin):
    model = Category

# Register your models here.

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
