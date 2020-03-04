from django.db import models
from django import forms
# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField


class CountryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        tag = request.GET.get('tag')
        countrypages = CountryPage.objects.filter(tags__name=tag)
     
        context = super().get_context(request)
        context['countrypages'] = countrypages
        return context



@register_snippet
class RiskCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Country'

    api_fields = [
        APIField('name'),
    ]



@register_snippet
class Region(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'region'

    api_fields = [
        APIField('name'),
    ]


class CountryPage(Page):

    # models
    country = models.CharField(max_length=250, blank=True, null=True)
    region = models.ForeignKey('country.Region', blank=True, null=True,on_delete=models.SET_NULL)
    body_en = RichTextField(blank=True)
    body_id = RichTextField(blank=True)
    risk_categories = ParentalManyToManyField('country.RiskCategory', blank=True)
    map_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('country'),
        index.SearchField('region'),
        index.SearchField('body_en'),
        index.SearchField('body_id'),

    ]

    content_panels = Page.content_panels + [
        FieldPanel('country'),
        FieldPanel('region'),
        MultiFieldPanel([
            FieldPanel('risk_categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Risk Category"),        
        ImageChooserPanel('map_image'),
        FieldPanel('body_en', classname="full"),
        FieldPanel('body_id', classname="full"),
        
    ]

    api_fields = [
        APIField('risk_categories'),
        APIField('country'),
        APIField('region'),
        APIField('map_image'),
        APIField('body_en'),
        APIField('body_id'),  
    ]


class CountryPageGalleryImage(Orderable):
    page = ParentalKey(CountryPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


