# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20150131_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendar',
            old_name='to_date',
            new_name='till_date',
        ),
        migrations.AlterField(
            model_name='calendarexception',
            name='calender',
            field=models.ForeignKey(related_name='exceptions', to='data.Calendar'),
            preserve_default=True,
        ),
    ]
