from .models import *
from modeltranslation.translator import register, TranslationOptions

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content', )

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )