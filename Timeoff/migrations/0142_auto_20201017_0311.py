# Generated by Django 3.0.8 on 2020-10-17 03:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0141_auto_20201017_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 10, 17, 3, 11, 34, 982965, tzinfo=utc)),
        ),
    ]
