# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20151015_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('popsize', models.IntegerField(verbose_name='Nombre de villageois requis', default=0)),
                ('textid', models.CharField(max_length=30, verbose_name='Type', default='Error')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('length', models.IntegerField(verbose_name='Required Time', default=0)),
                ('hometown', models.ForeignKey(to='game.Village')),
            ],
        ),
        migrations.RemoveField(
            model_name='expedition',
            name='hometown',
        ),
        migrations.DeleteModel(
            name='Expedition',
        ),
    ]
