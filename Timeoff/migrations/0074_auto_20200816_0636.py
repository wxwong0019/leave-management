# Generated by Django 3.0.8 on 2020-08-16 06:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0073_auto_20200815_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 16, 6, 36, 32, 533192, tzinfo=utc)),
        ),
    ]
