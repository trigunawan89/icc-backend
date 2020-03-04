from django.db import models
from django import forms
# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from django.utils.translation import ugettext as _
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtailgeowidget.edit_handlers import GeoPanel
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField
from wagtailautocomplete.edit_handlers import AutocompletePanel
from city.models import CityPage
from country.models import RiskCategory

class SiteIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        tag = request.GET.get('tag')
        siteypages = SitePage.objects.filter(tags__name=tag)
     
        context = super().get_context(request)
        context['siteypages'] = siteypages
        return context



@register_snippet
class SiteCategory(models.Model):
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
        verbose_name_plural = 'Business Unit'

    api_fields = [
        APIField('name'),
    ]


class SitePage(Page):

    # models
    site = models.CharField(max_length=250)
    city = models.ForeignKey('city.CityPage', blank=True, null=True,on_delete=models.SET_NULL)
    body_en = RichTextField(blank=True)
    body_id = RichTextField(blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)

    map_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('site'),
        index.SearchField('city'),
        index.SearchField('body_en'),
        index.SearchField('body_id'),

    ]

    content_panels = Page.content_panels + [

        FieldPanel('site'),
        AutocompletePanel('city'),     
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address'),
        ], _('Geo details')),
        ImageChooserPanel('map_image'),
        FieldPanel('body_en', classname="full"),
        FieldPanel('body_id', classname="full"),

    ]

    api_fields = [
        APIField('site'),
        APIField('city'),
        APIField('address'),
        APIField('location'),
        APIField('map_image'),
        APIField('body_en'),
        APIField('body_id'),  
    ]


class SitePageGalleryImage(Orderable):
    page = ParentalKey(SitePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


