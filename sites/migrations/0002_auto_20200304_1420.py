# Generated by Django 3.0.3 on 2020-03-04 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepage',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='sitepage',
            name='location',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
