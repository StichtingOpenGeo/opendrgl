# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20141227_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='planning_number',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trip',
            name='pattern',
            field=models.ForeignKey(related_name='trips', to='data.TripPattern'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trippattern',
            name='line',
            field=models.ForeignKey(related_name='patterns', to='data.Line'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trippatternstop',
            name='pattern',
            field=models.ForeignKey(related_name='stops', to='data.TripPattern'),
            preserve_default=True,
        ),
    ]
