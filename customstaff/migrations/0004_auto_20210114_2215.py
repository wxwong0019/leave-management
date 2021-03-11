# Generated by Django 3.0.8 on 2021-01-14 14:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customstaff', '0003_auto_20210114_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incrementall',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 424805, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='enddate',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 419735, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='endtime',
            field=models.TimeField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 419764, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='startdate',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 419671, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='starttime',
            field=models.TimeField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 419706, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='nonteachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 413288, tzinfo=utc)),
        ),
        migrations.RemoveField(
            model_name='nonteachingstaffdetail',
            name='supervisor',
        ),
        migrations.AddField(
            model_name='nonteachingstaffdetail',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor', to='customstaff.Supervisor'),
        ),
        migrations.AlterField(
            model_name='nonteachingstaffdetail',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='NonTeachingStaffDetail', to='customstaff.NonTeachingStaff'),
        ),
        migrations.AlterField(
            model_name='secretarydetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 414485, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='supervisordetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 415356, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='teachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 412077, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='viceprincipaldetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 1, 14, 14, 15, 23, 417094, tzinfo=utc)),
        ),
    ]
