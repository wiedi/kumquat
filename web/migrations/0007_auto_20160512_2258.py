# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20160512_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letsencrypt',
            name='vhost',
            field=annoying.fields.AutoOneToOneField(to='web.VHost', on_delete=models.CASCADE),
        ),
    ]
