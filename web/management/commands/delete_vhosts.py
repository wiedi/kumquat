from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import shutil
from subprocess import call, check_output


class Command(BaseCommand):
	args = ''
	help = 'remove webroots that have been marked for deletion'

	def handle(self, *args, **options):
		if settings.KUMQUAT_USE_ZFS:
			for vhost in os.listdir(settings.KUMQUAT_VHOST_ROOT):
				ds = settings.KUMQUAT_VHOST_DATASET + '/' + vhost
				delete_soon = check_output(['zfs', 'get', '-Hp', 'core:delete_soon', ds]).strip().split()
				if len(delete_soon) != 4: continue
				if delete_soon[2] == '1':
					call(['zfs', 'destroy', ds])
		else:
			trash = settings.KUMQUAT_VHOST_ROOT + '/.Trash/'
			shutil.rmtree(trash)
			os.mkdir(trash)