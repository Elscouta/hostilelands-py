# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expedition',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('popsize', models.IntegerField(verbose_name='Nombre de villageois', default=0)),
                ('goal', models.CharField(max_length=30, verbose_name='But', default='Error')),
                ('start_time', models.DateTimeField(verbose_name='Start Time')),
                ('length', models.IntegerField(verbose_name='Required Time', default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name', default='Undefined')),
                ('level', models.IntegerField(verbose_name='Level', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Village',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=30, verbose_name='Name', default='Undefined')),
                ('food', models.IntegerField(verbose_name='Food', default=0)),
                ('wood', models.IntegerField(verbose_name='Wood', default=0)),
                ('population', models.IntegerField(verbose_name='Population', default=10)),
                ('population_occ', models.IntegerField(verbose_name='Population working', default=0)),
                ('farm_level', models.IntegerField(verbose_name='Farm Level', default=1)),
                ('simulation_time', models.DateTimeField(verbose_name='Simulated Up To')),
            ],
        ),
        migrations.AddField(
            model_name='hero',
            name='hometown',
            field=models.ForeignKey(to='game.Village'),
        ),
        migrations.AddField(
            model_name='expedition',
            name='hometown',
            field=models.ForeignKey(to='game.Village'),
        ),
    ]
