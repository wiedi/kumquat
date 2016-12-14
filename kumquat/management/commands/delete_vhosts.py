from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import shutil
from subprocess import call


class Command(BaseCommand):
	args = ''
	help = 'remove webroots that have been marked for deletion'

	def handle(self, *args, **options):
		if settings.KUMQUAT_USE_ZFS:
			for vhost in os.listdir(settings.KUMQUAT_VHOST_ROOT + '/.Trash/'):
				call(['zfs', 'destroy', '-r', settings.KUMQUAT_VHOST_DATASET + '/.Trash/' + vhost])
		else:
			trash = settings.KUMQUAT_VHOST_ROOT + '/.Trash/'
			shutil.rmtree(trash)
			os.mkdir(trash)