# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20141023_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='city',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
    ]
