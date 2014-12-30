# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chb', '0002_auto_20141221_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chbquay',
            old_name='lng',
            new_name='lon',
        ),
    ]
