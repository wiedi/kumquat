import os
import re
import shutil
from subprocess import call, check_output
from gevent import monkey, lock, spawn
monkey.patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False, aggressive=True)
import zerorpc
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from django.conf import settings
from web.models import VHost, SSLCert, DefaultVHost
from update_vhosts import update_vhosts

update_lock = lock.RLock()
def locked_update_vhosts():
	with update_lock:
		update_vhosts()

class Backend(object):
	def update_vhosts(self):
		spawn(locked_update_vhosts)
	
	def snapshot_list(self, vhost):
		if not settings.KUMQUAT_USE_ZFS:
			raise Exception("Snapshots only supported with ZFS")

		v = get_object_or_404(VHost, pk = vhost)
		snapshots = []
		ds = settings.KUMQUAT_VHOST_DATASET + '/' + unicode(v)
		try:
			out = check_output(['zfs', 'list', '-o', 'name,creation,core:user_created', '-rpHt', 'snapshot', ds])
		except:
			return []
		for snap in out.strip().split("\n"):
			s = snap.split()
			if len(s) != 3: continue
			name, creation, user_created = s
			snapshots += [{
				'name':         name.split('@')[1],
				'creation':     int(creation),
				'user_created': user_created != '-',
			}]
		return snapshots
	
	def snapshot_create(self, vhost, name):
		if not settings.KUMQUAT_USE_ZFS:
			raise Exception("Snapshots only supported with ZFS")

		if not re.match(r'^([a-z0-9_-]+)$', name):
			raise Exception("Invalid snapshot name")

		v = get_object_or_404(VHost, pk = vhost)
		ds = settings.KUMQUAT_VHOST_DATASET + '/' + unicode(v)
		snap = ds + '@user_' + name
		try:
			check_output(['zfs', 'snapshot', snap])
			call(['zfs', 'set', 'core:user_created=1', snap])
		except:
			return False
		return True


	def snapshot_rollback(self, vhost, name):
		if not settings.KUMQUAT_USE_ZFS:
			raise Exception("Snapshots only supported with ZFS")

		v = get_object_or_404(VHost, pk = vhost)
		ds = settings.KUMQUAT_VHOST_DATASET + '/' + unicode(v)
		call(['zfs', 'rollback', '-r', ds + '@' + name])

	def snapshot_delete(self, vhost, name):
		if not settings.KUMQUAT_USE_ZFS:
			raise Exception("Snapshots only supported with ZFS")

		v = get_object_or_404(VHost, pk = vhost)
		ds = settings.KUMQUAT_VHOST_DATASET + '/' + unicode(v)
		snap = ds + '@' + name
		user_created = check_output(['zfs', 'get', '-Hp', 'core:user_created',  snap]).strip().split()[2]
		if user_created == '-':
			raise Exception("Only user created Snapshots can be deleted")
		call(['zfs', 'destroy', ds + '@' + name])


class Command(BaseCommand):
	args = ''
	help = 'run backend service'

	def handle(self, *args, **options):
		s = zerorpc.Server(Backend())
		s.bind(settings.KUMQUAT_BACKEND_SOCKET)
		s.run()
