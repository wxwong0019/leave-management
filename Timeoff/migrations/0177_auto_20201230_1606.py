# Generated by Django 3.0.8 on 2020-12-30 08:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0176_auto_20201230_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 30, 8, 6, 2, 591125, tzinfo=utc)),
        ),
    ]