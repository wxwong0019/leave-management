# Generated by Django 3.0.8 on 2021-01-14 13:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0186_auto_20210114_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 13, 44, 32, 796937, tzinfo=utc)),
        ),
    ]
