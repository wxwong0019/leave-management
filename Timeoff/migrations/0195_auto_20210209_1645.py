# Generated by Django 3.0.8 on 2021-02-09 08:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0194_auto_20210209_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 2, 9, 8, 45, 8, 684607, tzinfo=utc)),
        ),
    ]