# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kumquat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('subaddress', models.BooleanField(default=False, help_text='Enable subaddress extension (e.g. primary+sub@example.com', verbose_name='Subaddress extension')),
                ('domain', models.ForeignKey(related_name='mail_accounts', to='kumquat.Domain', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('to', models.CharField(max_length=255)),
                ('domain', models.ForeignKey(to='kumquat.Domain', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='redirect',
            unique_together=set([('name', 'domain')]),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('name', 'domain')]),
        ),
    ]
