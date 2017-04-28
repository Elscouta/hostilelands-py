# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_property'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completion',
            field=models.DecimalField(verbose_name='Completion', default=0, max_digits=16, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='property',
            name='value',
            field=models.DecimalField(verbose_name='Value', default=1, max_digits=16, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='village',
            name='food',
            field=models.DecimalField(verbose_name='Food', default=0, max_digits=16, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='village',
            name='wood',
            field=models.DecimalField(verbose_name='Wood', default=0, max_digits=16, decimal_places=3),
        ),
    ]
