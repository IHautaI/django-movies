# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.RemoveField(
            model_name='rater',
            name='mid',
        ),
        migrations.AddField(
            model_name='movie',
            name='title',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='ratings.Genre'),
        ),
    ]
