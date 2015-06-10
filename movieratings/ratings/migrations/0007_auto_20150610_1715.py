# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0006_auto_20150610_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rater',
            name='zip_code',
            field=models.CharField(verbose_name='zipcode', max_length=40),
        ),
    ]
