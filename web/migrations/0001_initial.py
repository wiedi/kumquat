# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import kumquat.utils


class Migration(migrations.Migration):

    dependencies = [
        ('kumquat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultVHost',
            fields=[
                ('domain', models.OneToOneField(primary_key=True, serialize=False, to='kumquat.Domain', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SSLCert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cn', models.CharField(max_length=255)),
                ('serial', models.CharField(max_length=255)),
                ('valid_not_before', models.DateTimeField()),
                ('valid_not_after', models.DateTimeField()),
                ('subject', models.CharField(max_length=255)),
                ('issuer', models.CharField(max_length=255)),
                ('cert', models.TextField()),
                ('key', models.TextField()),
                ('ca', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Child part of your domain that is used to organize your site content.', max_length=255, verbose_name='Sub Domain', validators=[kumquat.utils.DomainNameValidator()])),
                ('cert', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'SSL Certificate', blank=True, to='web.SSLCert', null=True)),
                ('domain', models.ForeignKey(to='kumquat.Domain', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='defaultvhost',
            name='vhost',
            field=models.ForeignKey(to='web.VHost', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='vhost',
            unique_together=set([('name', 'domain')]),
        ),
    ]
