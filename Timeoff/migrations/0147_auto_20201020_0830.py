# Generated by Django 3.0.8 on 2020-10-20 08:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0146_auto_20201019_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 10, 20, 8, 30, 0, 107062, tzinfo=utc)),
        ),
    ]