# Generated by Django 3.0.8 on 2020-08-10 08:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Timeoff', '0018_auto_20200810_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeoff',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 8, 10, 8, 52, 48, 45791, tzinfo=utc)),
        ),
    ]