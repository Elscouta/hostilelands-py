# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='context',
            field=models.TextField(verbose_name='Context', default='{}', max_length=500),
        ),
    ]
