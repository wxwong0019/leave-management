# Generated by Django 3.0.8 on 2021-02-10 12:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0198_auto_20210210_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 473576, tzinfo=utc)),
        ),
    ]
