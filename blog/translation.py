from .models import BlogPage, BlogIndexPage
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register



@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    fields = (
        'intro',
    )

@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        'body',
    )

