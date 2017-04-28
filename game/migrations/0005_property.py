# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20151021_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('textid', models.CharField(max_length=80, verbose_name='Identifier', default='Undefined')),
                ('value', models.IntegerField(verbose_name='Value', default=1)),
                ('hometown', models.ForeignKey(to='game.Village')),
            ],
        ),
    ]
