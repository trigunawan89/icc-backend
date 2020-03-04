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
from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField

# import country
from country.models import CountryPage


class AdvisoryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        tag = request.GET.get('tag')
        advisorypages = AdvisoryPage.objects.filter(tags__name=tag)
     
        context = super().get_context(request)
        context['advisorypages'] = advisorypages
        return context


class AdvisoryPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'AdvisoryPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


@register_snippet
class AdvisoryCategory(models.Model):
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
        verbose_name_plural = 'advisory categories'

    api_fields = [
        APIField('name'),
    ]



class AdvisoryPage(Page):
    date = models.DateField("Post date")
    title_id = models.CharField(max_length=250)
    body_en = RichTextField(blank=True)
    body_id = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=AdvisoryPageTag, blank=True)
    categories = models.ForeignKey('advisory.AdvisoryCategory', blank=True, null=True,on_delete=models.SET_NULL)
    country = models.ForeignKey('country.CountryPage', blank=True, null=True,on_delete=models.SET_NULL)
    remark = models.CharField(max_length=250, blank=True)

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    search_fields = Page.search_fields + [
        index.SearchField('title_id'),
        index.SearchField('body_en'),
        index.SearchField('body_id'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('title_id'),
        AutocompletePanel('country'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories'),
        ], heading="Advisory information"),        
        ImageChooserPanel('feed_image'),
        FieldPanel('body_en', classname="full"),
        FieldPanel('body_id', classname="full"),
        FieldPanel('remark'),
        
    ]

    api_fields = [
        APIField('date'),
        APIField('categories'),
        APIField('country'),
        APIField('title_id'),
        APIField('feed_image'),
        APIField('body_en'),
        APIField('body_id'),
        APIField('remark'),
    ]

class AdvisoryPageGalleryImage(Orderable):
    page = ParentalKey(AdvisoryPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
