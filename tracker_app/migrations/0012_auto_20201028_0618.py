# Generated by Django 3.1.2 on 2020-10-27 19:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0011_auto_20201020_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='group',
            name='expiry',
            field=models.DateField(default=datetime.datetime(2021, 2, 17, 6, 18, 59, 116013)),
        ),
        migrations.CreateModel(
            name='ReportIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('dateSubmitted', models.DateField(default=datetime.datetime.today)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker_app.group')),
                ('groupMember', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker_app.groupmember')),
            ],
        ),
    ]