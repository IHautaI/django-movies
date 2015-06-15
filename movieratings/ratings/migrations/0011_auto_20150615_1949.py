# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0010_auto_20150615_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='rater',
            name='descr',
            field=models.CharField(max_length=511, default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='genre',
            name='movies',
            field=models.ManyToManyField(to='ratings.Movie'),
        ),
    ]
