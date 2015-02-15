# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarException',
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
        migrations.RemoveField(
            model_name='calenderexceptions',
            name='calender',
        ),
        migrations.DeleteModel(
            name='CalenderExceptions',
        ),
        migrations.AddField(
            model_name='calendar',
            name='label',
            field=models.CharField(default='<imported>', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
