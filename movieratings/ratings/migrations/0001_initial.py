# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('mid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('uid', models.IntegerField()),
                ('mid', models.ManyToManyField(to='ratings.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('rating', models.IntegerField()),
                ('timestamp', models.DateField()),
                ('mid', models.ForeignKey(to='ratings.Movie')),
                ('uid', models.ForeignKey(to='ratings.Rater')),
            ],
        ),
    ]
