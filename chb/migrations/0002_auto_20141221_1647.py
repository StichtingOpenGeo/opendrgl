# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chb', '0001_squashed_0004_auto_20141214_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chbquay',
            name='city',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chbquay',
            name='public_code',
            field=models.CharField(unique=True, max_length=13),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chbquay',
            name='stop',
            field=models.ForeignKey(related_name='quays', to='chb.ChbStop'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='chbstop',
            name='type',
            field=models.CharField(max_length=25),
            preserve_default=True,
        ),
    ]
