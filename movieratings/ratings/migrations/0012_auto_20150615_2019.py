# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0011_auto_20150615_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='descr',
            field=models.CharField(max_length=511, default=' '),
        ),
        migrations.AddField(
            model_name='rating',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
