# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0004_auto_20150610_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
