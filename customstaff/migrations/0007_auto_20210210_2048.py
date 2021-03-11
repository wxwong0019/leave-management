# Generated by Django 3.0.8 on 2021-02-10 12:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customstaff', '0006_auto_20210117_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incrementall',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 495071, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='enddate',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 489128, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='endtime',
            field=models.TimeField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 489154, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='startdate',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 489067, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='starttime',
            field=models.TimeField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 489098, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='nonteachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 481753, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='secretarydetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 482885, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='supervisordetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 483900, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='teachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 480724, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='viceprincipaldetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 10, 12, 48, 28, 486407, tzinfo=utc)),
        ),
    ]