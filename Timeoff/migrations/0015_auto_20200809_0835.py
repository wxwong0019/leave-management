# Generated by Django 3.0.8 on 2020-08-09 08:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0014_auto_20200809_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 9, 8, 35, 23, 268580, tzinfo=utc)),
        ),
    ]
