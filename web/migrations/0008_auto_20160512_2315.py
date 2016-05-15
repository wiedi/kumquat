# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20160512_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letsencrypt',
            name='state',
            field=models.CharField(default=b'REQUESTED', max_length=255),
        ),
    ]
