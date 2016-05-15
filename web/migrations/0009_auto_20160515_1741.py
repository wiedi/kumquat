# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20160512_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letsencrypt',
            name='last_message',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='letsencrypt',
            name='state',
            field=models.CharField(default=b'REQUESTED', max_length=255, choices=[(b'REQUESTED', b'Requested'), (b'VALID', b'Valid'), (b'EXPIRE_SOON', b'Expire soon')]),
        ),
    ]
