# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(default='Error', max_length=30, verbose_name='Name')),
                ('level', models.IntegerField(default=0, verbose_name='Level')),
            ],
        ),
        migrations.RemoveField(
            model_name='village',
            name='farm_level',
        ),
        migrations.AddField(
            model_name='building',
            name='hometown',
            field=models.ForeignKey(to='game.Village'),
        ),
    ]
