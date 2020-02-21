# Generated by Django 3.0.3 on 2020-02-21 02:14

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200220_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpage',
            old_name='body',
            new_name='body_en',
        ),
        migrations.RenameField(
            model_name='blogpage',
            old_name='intro',
            new_name='intro_en',
        ),
        migrations.RemoveField(
            model_name='blogindexpage',
            name='intro_en_us',
        ),
        migrations.RemoveField(
            model_name='blogindexpage',
            name='intro_ind',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='body_en_us',
        ),
        migrations.RemoveField(
            model_name='blogpage',
            name='body_ind',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='body_id',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='intro_id',
            field=models.CharField(default='Hello', max_length=250),
            preserve_default=False,
        ),
    ]