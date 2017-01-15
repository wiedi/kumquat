from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.conf import settings
from web.models import SSLCert, VHost, LetsEncrypt
from subprocess import call
from free_tls_certificates import client
from django.utils import timezone
from cProfile import Profile
import requests.exceptions
import acme.messages
import uuid
import os
import io
import pstats
import re
if settings.KUMQUAT_USE_0RPC:
	import zerorpc

def issue_cert():
	letsencrypt_issued = False
	for vhost in VHost.objects.filter(use_letsencrypt=True):
		if vhost.letsencrypt_state() not in ['REQUEST', 'RENEW']:
			continue
		try:
			data = client.issue_certificate(
				[str(vhost),] + list(vhost.vhostalias_set.values_list('alias', flat=True)),
				settings.LETSENCRYPT_STATE_FOLDER,
				agree_to_tos_url = settings.LETSENCRYPT_TOS,
				acme_server = settings.LETSENCRYPT_ACME_SERVER)

			chain = "\n".join(data['chain'])
			cert = SSLCert()
			cert.set_cert(cert=data['cert'], key=data['private_key'], ca=chain)
			cert.save()

			vhost.cert = cert
			vhost.save()

			vhost.letsencrypt.last_message = ''
			vhost.letsencrypt.save()

			letsencrypt_issued = True

		except client.NeedToTakeAction as e:
			vhost.letsencrypt.last_message = str(e)
			vhost.letsencrypt.save()
			for action in e.actions:
				if isinstance(action, client.NeedToInstallFile):
					file_name = re.sub(r'[^\w-]', '', action.file_name)
					with open(settings.LETSENCRYPT_ACME_FOLDER + '/' + file_name, 'w') as f:
						f.write(action.contents)
		except Exception as e:
			vhost.letsencrypt.last_message = str(e)
			vhost.letsencrypt.save()

	if letsencrypt_issued and settings.KUMQUAT_USE_0RPC:
		zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET).update_vhosts()

class Command(BaseCommand):
	args = ''
	help = 'issue lets encrypt ssl certificates'

	def add_arguments(self, parser):
		parser.add_argument('--profile', dest='profile', default=False, action='store_true')

	def handle(self, *args, **options):
		if options['profile']:
			profiler = Profile()
			profiler.runcall(issue_cert)
			pstats.Stats(profiler).sort_stats('cumulative').print_stats(25)
			return
		issue_cert()
