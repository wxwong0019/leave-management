# Generated by Django 3.0.8 on 2020-11-08 08:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0163_auto_20201108_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 11, 8, 8, 12, 58, 267095, tzinfo=utc)),
        ),
    ]
