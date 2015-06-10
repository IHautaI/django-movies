# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_auto_20150609_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='mid',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='uid',
            new_name='rater',
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.FloatField(),
        ),
    ]
