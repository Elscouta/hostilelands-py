# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20151016_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='name',
            new_name='textid',
        ),
    ]
