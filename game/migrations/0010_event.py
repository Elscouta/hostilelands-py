# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20151209_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('textid', models.CharField(default='Undefined', max_length=30, verbose_name='Event Identifier')),
                ('context', models.BinaryField(default='{}', max_length=500, verbose_name='Context')),
                ('time', models.DateTimeField(verbose_name='Time of event')),
                ('unread', models.BooleanField(default=True, verbose_name='Is Unread')),
                ('hometown', models.ForeignKey(to='game.Village')),
            ],
        ),
    ]
