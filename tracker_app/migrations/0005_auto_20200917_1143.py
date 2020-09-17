# Generated by Django 3.1.1 on 2020-09-17 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0004_auto_20200916_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskcategory',
            name='submittedBy',
        ),
        migrations.AddField(
            model_name='memberentry',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker_app.taskcategory'),
        ),
    ]
