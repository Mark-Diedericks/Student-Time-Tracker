# Generated by Django 3.1.1 on 2020-10-12 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0009_submittedperiod'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedperiod',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker_app.group'),
        ),
    ]
