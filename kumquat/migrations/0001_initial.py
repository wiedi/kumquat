# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kumquat.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Your primary domain (example.com) that you like to use for the different services.', unique=True, max_length=255, verbose_name='Name', validators=[kumquat.utils.DomainNameValidator()])),
            ],
        ),
    ]
