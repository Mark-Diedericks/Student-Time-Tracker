# Generated by Django 3.1.1 on 2020-10-29 07:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0017_auto_20201029_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 2, 18, 18, 33, 14, 468618)),
        ),
    ]
