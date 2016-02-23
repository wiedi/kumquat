# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cronjob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when', models.CharField(max_length=255, verbose_name='When', choices=[(b'0,5,10,15,20,25,30,35,40,45,50,55 * * * *', 'every 5 minutes'), (b'0,30 * * * *', 'every 30 minutes'), (b'0 * * * *', 'hourly'), (b'0 0 * * *', 'daily'), (b'0 0 * * 0', 'weekly'), (b'0 0 1 * *', 'monthly')])),
                ('command', models.CharField(help_text='Posix shell command which will be exectured', max_length=1024, verbose_name='Command')),
            ],
        ),
    ]
