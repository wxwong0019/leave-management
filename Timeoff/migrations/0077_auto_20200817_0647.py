# Generated by Django 3.0.8 on 2020-08-17 06:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0076_auto_20200817_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 17, 6, 47, 4, 681801, tzinfo=utc)),
        ),
    ]
