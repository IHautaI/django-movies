# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0005_auto_20150610_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='mid',
        ),
        migrations.RemoveField(
            model_name='rater',
            name='uid',
        ),
    ]
