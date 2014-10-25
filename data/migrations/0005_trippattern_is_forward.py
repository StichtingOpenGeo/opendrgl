# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20141024_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='trippattern',
            name='is_forward',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
