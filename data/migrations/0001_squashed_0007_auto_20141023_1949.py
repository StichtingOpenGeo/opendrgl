# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'data', '0001_initial'), (b'data', '0002_auto_20141023_1943'), (b'data', '0003_auto_20141023_1944'), (b'data', '0004_auto_20141023_1945'), (b'data', '0005_auto_20141023_1947'), (b'data', '0006_auto_20141023_1948'), (b'data', '0007_auto_20141023_1949')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datacode', models.CharField(unique=True, max_length=5)),
                ('name', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('on_monday', models.BooleanField(default=False)),
                ('on_tuesday', models.BooleanField(default=False)),
                ('on_wednesday', models.BooleanField(default=False)),
                ('on_thursday', models.BooleanField(default=False)),
                ('on_friday', models.BooleanField(default=False)),
                ('on_saturday', models.BooleanField(default=False)),
                ('on_sunday', models.BooleanField(default=False)),
                ('agency', models.ForeignKey(to='data.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CalenderExceptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_cancel', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('calender', models.ForeignKey(to='data.Calendar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('planning_number', models.CharField(max_length=10)),
                ('public_number', models.PositiveSmallIntegerField()),
                ('agency', models.ForeignKey(to='data.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public_number', models.CharField(unique=True, max_length=10)),
                ('planning_number', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=25)),
                ('lat', models.DecimalField(max_digits=10, decimal_places=8)),
                ('lng', models.DecimalField(max_digits=10, decimal_places=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StopProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=10)),
                ('value', models.TextField()),
                ('stop', models.ForeignKey(to='data.Stop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField()),
                ('calendar', models.ForeignKey(to='data.Calendar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripPattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line', models.ForeignKey(to='data.Line')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripPatternStop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('arrival_delta', models.PositiveIntegerField()),
                ('departure_delta', models.PositiveIntegerField()),
                ('pattern', models.ForeignKey(to='data.TripPattern')),
                ('stop', models.ForeignKey(to='data.Stop')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='trippatternstop',
            unique_together=set([('pattern', 'order')]),
        ),
        migrations.AddField(
            model_name='trip',
            name='trip_pattern',
            field=models.ForeignKey(to='data.TripPattern'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='trip',
            unique_together=set([('trip_pattern', 'start_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='stopproperty',
            unique_together=set([('stop', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='line',
            unique_together=set([('agency', 'planning_number')]),
        ),
        migrations.AddField(
            model_name='stop',
            name='agency',
            field=models.ForeignKey(default=None, to='data.Agency'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stop',
            name='public_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='stop',
            unique_together=set([('agency', 'public_number')]),
        ),
        migrations.AlterField(
            model_name='stop',
            name='lat',
            field=models.DecimalField(max_digits=10, decimal_places=8, blank=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='lng',
            field=models.DecimalField(max_digits=10, decimal_places=8, blank=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='lat',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=8, blank=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='lng',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=8, blank=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='calendar',
            field=models.ForeignKey(to='data.Calendar', blank=True),
        ),
        migrations.AlterField(
            model_name='trippatternstop',
            name='arrival_delta',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='trippatternstop',
            name='departure_delta',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='calendar',
            field=models.ForeignKey(blank=True, to='data.Calendar', null=True),
        ),
        migrations.AlterField(
            model_name='trippatternstop',
            name='arrival_delta',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='trippatternstop',
            name='departure_delta',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
