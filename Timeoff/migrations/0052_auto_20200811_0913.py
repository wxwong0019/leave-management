# Generated by Django 3.0.8 on 2020-08-11 09:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0051_auto_20200811_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 11, 9, 13, 45, 57664, tzinfo=utc)),
        ),
    ]