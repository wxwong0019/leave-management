# Generated by Django 3.0.8 on 2020-09-09 13:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0123_auto_20200909_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 9, 9, 13, 26, 6, 490478, tzinfo=utc)),
        ),
    ]
