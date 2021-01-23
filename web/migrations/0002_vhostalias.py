# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kumquat.utils


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VHostAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(help_text='Full alias domain name for virtual host.', max_length=255, verbose_name='Alias', validators=[kumquat.utils.DomainNameValidator()])),
                ('vhost', models.ForeignKey(to='web.VHost', on_delete=models.CASCADE)),
            ],
        ),
    ]
