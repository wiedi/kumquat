# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20160512_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='vhost',
            name='letsencrypt',
            field=models.BooleanField(default=False, verbose_name="SSL Certificate managed by Let's Encrypt"),
        ),
    ]
