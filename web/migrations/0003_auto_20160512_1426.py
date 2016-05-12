# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kumquat.utils


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_vhostalias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vhostalias',
            name='alias',
            field=models.CharField(help_text='Full alias domain name for virtual host.', unique=True, max_length=255, verbose_name='Alias', validators=[kumquat.utils.DomainNameValidator()]),
        ),
    ]
