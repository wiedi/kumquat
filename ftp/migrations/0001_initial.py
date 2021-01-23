# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('path', models.CharField(default=b'/', max_length=255)),
                ('vhost', models.ForeignKey(blank=True, to='web.VHost', null=True, on_delete=models.CASCADE)),
            ],
        ),
    ]
