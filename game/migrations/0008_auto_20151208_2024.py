# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20151205_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='textid',
            field=models.CharField(max_length=80, default='Error', verbose_name='Type'),
        ),
    ]
