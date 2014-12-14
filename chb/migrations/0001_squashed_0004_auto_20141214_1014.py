# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'chb', '0001_initial'), (b'chb', '0002_auto_20141214_1010'), (b'chb', '0003_auto_20141214_1011'), (b'chb', '0004_auto_20141214_1014')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChbQuay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public_number', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=25, null=True, blank=True)),
                ('lat', models.DecimalField(null=True, max_digits=10, decimal_places=8, blank=True)),
                ('lng', models.DecimalField(null=True, max_digits=10, decimal_places=8, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChbStop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('public_code', models.CharField(unique=True, max_length=13)),
                ('type', models.CharField(default='type', max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chbquay',
            name='stop',
            field=models.ForeignKey(to='chb.ChbStop'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='chbquay',
            old_name='public_number',
            new_name='public_code',
        ),
    ]
