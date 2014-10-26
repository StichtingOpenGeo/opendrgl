# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_trippattern_is_forward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='start_time',
            field=models.IntegerField(),
        ),
    ]
