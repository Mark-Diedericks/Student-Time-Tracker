# Generated by Django 3.1.1 on 2020-09-16 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0002_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]