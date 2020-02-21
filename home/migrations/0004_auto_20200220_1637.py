# Generated by Django 3.0.3 on 2020-02-20 09:37

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body_en_us',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='body_ind',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]