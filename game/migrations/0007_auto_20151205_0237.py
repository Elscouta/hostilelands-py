# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20151023_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommitedRessource',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('quantity', models.DecimalField(verbose_name='Amount', max_digits=16, default=0, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='Ressource',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('textid', models.CharField(max_length=30, verbose_name='Ressource Identifier', default='Undefined')),
                ('total', models.DecimalField(verbose_name='Total', max_digits=16, default=0, decimal_places=3)),
                ('occupied', models.DecimalField(verbose_name='Occupied', max_digits=16, default=0, decimal_places=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='popsize',
        ),
        migrations.RemoveField(
            model_name='village',
            name='food',
        ),
        migrations.RemoveField(
            model_name='village',
            name='population',
        ),
        migrations.RemoveField(
            model_name='village',
            name='population_occ',
        ),
        migrations.RemoveField(
            model_name='village',
            name='wood',
        ),
        migrations.AddField(
            model_name='ressource',
            name='hometown',
            field=models.ForeignKey(to='game.Village'),
        ),
        migrations.AddField(
            model_name='commitedressource',
            name='ressource',
            field=models.ForeignKey(to='game.Ressource'),
        ),
        migrations.AddField(
            model_name='commitedressource',
            name='task',
            field=models.ForeignKey(to='game.Task'),
        ),
    ]
