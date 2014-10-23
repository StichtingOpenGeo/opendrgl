# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_squashed_0007_auto_20141023_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trippattern',
            name='line',
            field=models.ForeignKey(related_name=b'trippatterns', to='data.Line'),
        ),
    ]
