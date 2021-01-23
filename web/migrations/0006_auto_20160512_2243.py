# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_vhost_letsencrypt'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetsEncrypt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=255)),
                ('last_message', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='vhost',
            old_name='letsencrypt',
            new_name='use_letsencrypt',
        ),
        migrations.AddField(
            model_name='letsencrypt',
            name='vhost',
            field=models.OneToOneField(to='web.VHost', on_delete=models.CASCADE),
        ),
    ]
