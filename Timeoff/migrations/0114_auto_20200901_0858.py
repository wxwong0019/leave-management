# Generated by Django 3.0.8 on 2020-09-01 08:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0113_auto_20200901_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 1, 8, 58, 57, 628955, tzinfo=utc)),
        ),
    ]