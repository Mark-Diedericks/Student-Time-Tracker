# Generated by Django 3.1.1 on 2020-09-23 02:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0007_auto_20200923_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberentry',
            old_name='date',
            new_name='entered',
        ),
        migrations.AddField(
            model_name='group',
            name='created',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
