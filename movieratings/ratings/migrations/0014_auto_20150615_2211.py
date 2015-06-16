# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0013_auto_20150615_2210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rater',
            old_name='descr',
            new_name='description',
        ),
    ]
