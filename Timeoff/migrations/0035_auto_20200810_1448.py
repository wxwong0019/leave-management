# Generated by Django 3.0.8 on 2020-08-10 14:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0034_auto_20200810_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 10, 14, 48, 18, 665143, tzinfo=utc)),
        ),
    ]
