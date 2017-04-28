# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20151208_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='textid',
            new_name='base_textid',
        ),
        migrations.AddField(
            model_name='task',
            name='params',
            field=models.CharField(max_length=80, default='', verbose_name='Params'),
        ),
    ]
