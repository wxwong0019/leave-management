# Generated by Django 3.0.8 on 2021-03-01 04:30

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customstaff', '0009_auto_20210221_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonteachingstaffdetail',
            name='viceprincipal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='viceprincipal', to='customstaff.VicePrincipal'),
        ),
        migrations.AlterField(
            model_name='incrementall',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 266321, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='enddate',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 259934, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='endtime',
            field=models.TimeField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 259968, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='startdate',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 259852, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='starttime',
            field=models.TimeField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 259897, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='nonteachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 254391, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='secretarydetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 255375, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='supervisordetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 256181, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='teachingstaffdetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 253521, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='viceprincipaldetail',
            name='firstday',
            field=models.DateField(default=datetime.datetime(2021, 3, 1, 4, 30, 9, 257651, tzinfo=utc)),
        ),
    ]
