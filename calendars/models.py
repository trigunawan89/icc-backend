from django.db import models
from django import forms
# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from wagtail.snippets.models import register_snippet
from wagtail.api import APIField

# import country
from country.models import CountryPage


class CalendarIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        tag = request.GET.get('tag')
        calendarpages = CalendarPage.objects.filter(tags__name=tag)
     
        context = super().get_context(request)
        context['calendarpages'] = calendarpages
        return context


class CalendarPage(Page):
    date_from = models.DateField("Date From")
    date_to = models.DateField("Date To")
    title_id = models.CharField(max_length=250)
    country = ParentalManyToManyField('country.CountryPage', blank=True)
    body_en = RichTextField(blank=True)
    body_id = RichTextField(blank=True)
    remark = models.CharField(max_length=250, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('country'),
        index.SearchField('body_en'),
        index.SearchField('body_id'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('title_id'),
        FieldPanel('country', widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel([
            FieldPanel('date_from'),
            FieldPanel('date_to'),
        ], heading="Date of Event"),        
        FieldPanel('body_en', classname="full"),
        FieldPanel('body_id', classname="full"),
        FieldPanel('remark'),
        
    ]

    api_fields = [
        APIField('title_id'),
        APIField('date_from'),
        APIField('date_to'),
        APIField('country'),
        APIField('body_en'),
        APIField('body_id'),
        APIField('remark'),
    ]

