from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.template.loader import render_to_string
from django.conf import settings
from web.models import SSLCert, VHost
from subprocess import call
import uuid
import os
import time

def write_certs():
	file_list = []
	for cert in SSLCert.objects.filter(vhost__isnull = False).distinct():
		cert.write_bundle()
		file_list += [os.path.basename(cert.bundle_name())]
	for f in os.listdir(settings.KUMQUAT_CERT_PATH):
		if f not in file_list:
			os.unlink(settings.KUMQUAT_CERT_PATH + '/' + f)

def write_vhost_config():
	config = ''
	for vhost in VHost.objects.filter(is_enabled = True).annotate(is_defaultvhost=Count('defaultvhost')).order_by('is_defaultvhost'):
		context = {
			'vhost': vhost,
		}
		try:
			config += render_to_string('web/vhost-' + str(vhost.punycode()) + '.conf', context)
		except:
			config += render_to_string('web/vhost.conf', context)

	with open(settings.KUMQUAT_VHOST_CONFIG, 'w') as f:
		f.write(config)

def reload_webserver():
	call(settings.KUMQUAT_WEBSERVER_RELOAD, shell=True)

def webroot(vhost):
	return os.path.abspath(settings.KUMQUAT_VHOST_ROOT + '/' + vhost)

def webroot_dataset(vhost):
	return settings.KUMQUAT_VHOST_DATASET + '/' + vhost

def update_vhosts():
	dirs   = set(os.listdir(settings.KUMQUAT_VHOST_ROOT)) - set(['.Trash'])
	vhosts = set([str(vhost.punycode()) for vhost in VHost.objects.all()])

	remove = dirs - vhosts
	create = vhosts - dirs

	for vhost in create:
		if settings.KUMQUAT_USE_ZFS:
			call(['zfs', 'create', webroot_dataset(vhost)])
		else:
			os.makedirs(webroot(vhost))
		os.makedirs(webroot(vhost) + '/htdocs')
		os.makedirs(webroot(vhost) + '/logs')
		for p in [webroot(vhost), webroot(vhost) + '/logs', webroot(vhost) + '/htdocs']:
			os.chown(p, settings.KUMQUAT_VHOST_UID, settings.KUMQUAT_VHOST_GID)
		if settings.KUMQUAT_VHOST_POST_CREATE_CMD:
			call(settings.KUMQUAT_VHOST_POST_CREATE_CMD + [webroot(vhost)])

	write_certs()
	write_vhost_config()
	reload_webserver()

	# wait for a bit to give the webserver a chance to close it's logfiles
	time.sleep(5)

	for vhost in remove:
		deleted_name_suffix = '/.Trash/' + vhost + '-' + str(uuid.uuid4())
		if settings.KUMQUAT_USE_ZFS:
			call(['zfs', 'rename', '-fp', webroot_dataset(vhost), settings.KUMQUAT_VHOST_DATASET + deleted_name_suffix])
		else:
			os.rename(webroot(vhost), settings.KUMQUAT_VHOST_ROOT + deleted_name_suffix)
		if settings.KUMQUAT_VHOST_POST_DELETE_CMD:
			call(settings.KUMQUAT_VHOST_POST_DELETE_CMD + [webroot(vhost)])

class Command(BaseCommand):
	args = ''
	help = 'generate new vhosts config, rehash webserver and create webroots'

	def handle(self, *args, **options):
		update_vhosts()
