# Generated by Django 3.0.8 on 2020-09-09 12:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0120_auto_20200908_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 9, 12, 16, 11, 561465, tzinfo=utc)),
        ),
    ]
