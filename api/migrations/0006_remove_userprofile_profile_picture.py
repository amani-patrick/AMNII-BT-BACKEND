# Generated by Django 5.1.5 on 2025-02-08 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
