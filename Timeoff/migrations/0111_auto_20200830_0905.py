# Generated by Django 3.0.8 on 2020-08-30 09:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0110_auto_20200830_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 30, 9, 5, 55, 30514, tzinfo=utc)),
        ),
    ]
