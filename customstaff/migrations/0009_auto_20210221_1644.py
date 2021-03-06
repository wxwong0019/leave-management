# Generated by Django 3.0.8 on 2021-02-21 08:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customstaff', '0008_auto_20210221_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incrementall',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 317983, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='enddate',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 313504, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='endtime',
            field=models.TimeField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 313525, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='startdate',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 313453, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='starttime',
            field=models.TimeField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 313479, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='nonteachingstaffdetail',
            name='compensatedleave',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Compensated Leave Available (Hours)'),
        ),
        migrations.AlterField(
            model_name='nonteachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 308159, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='secretarydetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 309091, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='supervisordetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 309902, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='teachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 307327, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='viceprincipaldetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 2, 21, 8, 44, 54, 311351, tzinfo=utc)),
        ),
    ]
