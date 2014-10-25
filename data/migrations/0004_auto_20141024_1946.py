# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20141024_0941'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='trip_pattern',
            new_name='pattern',
        ),
        migrations.AlterUniqueTogether(
            name='trip',
            unique_together=set([('pattern', 'start_time')]),
        ),
    ]
