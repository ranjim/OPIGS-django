# Generated by Django 4.2 on 2023-04-07 08:03

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('core', '0006_alter_alumni_options_alter_company_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
