# Generated by Django 3.0.8 on 2020-08-11 03:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0036_auto_20200810_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 11, 3, 17, 19, 803895, tzinfo=utc)),
        ),
    ]
