# Generated by Django 4.2 on 2023-04-08 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_contact_mail_content_alter_contact_sender_mail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='', max_length=30),
        ),
    ]
