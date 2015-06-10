# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0003_auto_20150609_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='rater',
            name='age',
            field=models.IntegerField(default=0, verbose_name='age'),
        ),
        migrations.AddField(
            model_name='rater',
            name='zip_code',
            field=models.IntegerField(default=0, verbose_name='zipcode'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='rater',
            name='uid',
            field=models.IntegerField(verbose_name='User ID'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('movie', 'rater')]),
        ),
    ]
