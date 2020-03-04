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
from wagtail.documents.models import Document, AbstractDocument

# import country
from advisory.models import AdvisoryCategory


class GuidelineIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        tag = request.GET.get('tag')
        guidelinepage = GuidelinePage.objects.filter(tags__name=tag)
     
        context = super().get_context(request)
        context['guidelinepage'] = guidelinepage
        return context


class GuidelinePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'GuidelinePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class GuidelinePage(Page):
    date = models.DateField("Post date")
    title_id = models.CharField(max_length=250)
    body_en = RichTextField(blank=True)
    body_id = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=GuidelinePageTag, blank=True)
    categories = ParentalManyToManyField('advisory.AdvisoryCategory', blank=True)
    remark = models.CharField(max_length=250, blank=True)

    image = models.ForeignKey(
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
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Guideline information"),        
        ImageChooserPanel('image'),
        FieldPanel('body_en', classname="full"),
        FieldPanel('body_id', classname="full"),
        FieldPanel('remark'),
        
    ]

    api_fields = [
        APIField('date'),
        APIField('categories'),
        APIField('title_id'),
        APIField('image'),
        APIField('body_en'),
        APIField('body_id'),
        APIField('remark'),
        APIField('attachment',)
    ]

class GuidelinePageGalleryImage(Orderable):
    page = ParentalKey(GuidelinePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
