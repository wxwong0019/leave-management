# Generated by Django 3.0.8 on 2021-01-14 13:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0184_auto_20210114_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 13, 27, 1, 153422, tzinfo=utc)),
        ),
    ]