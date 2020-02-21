from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.api import APIField

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class BlogPage(Page):
    date = models.DateField("Post date")

    title_id = models.CharField(max_length=250)

    intro_en = models.CharField(max_length=250)
    intro_id = models.CharField(max_length=250)
    body_en = RichTextField(blank=True)
    body_id = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro_en'),
        index.SearchField('body_en'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('title_id'),
        FieldPanel('date'),
        FieldPanel('intro_en'),
        FieldPanel('body_en', classname="full"),
        FieldPanel('intro_id'),
        FieldPanel('body_id', classname="full"),
    ]

    api_fields = [
        APIField('date'),
        APIField('title'),
        APIField('title_id'),
        APIField('intro_en'),
        APIField('body_en'),
        APIField('intro_id'),
        APIField('body_id'),
        
    ]