# Generated by Django 3.1.1 on 2020-10-19 14:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0010_submittedperiod_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 2, 9, 1, 59, 4, 880434)),
        ),
        migrations.AlterField(
            model_name='group',
            name='created',
            field=models.DateField(default=datetime.datetime(2020, 10, 20, 1, 59, 4, 880434)),
        ),
    ]
