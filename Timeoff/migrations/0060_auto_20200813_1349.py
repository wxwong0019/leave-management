# Generated by Django 3.0.8 on 2020-08-13 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0059_auto_20200813_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 13, 13, 49, 49, 442490, tzinfo=utc)),
        ),
    ]
