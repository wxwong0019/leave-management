# Generated by Django 3.0.8 on 2020-08-11 07:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0038_auto_20200811_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 11, 7, 45, 39, 818620, tzinfo=utc)),
        ),
    ]