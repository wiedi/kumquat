from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.conf import settings
from web.models import SSLCert, VHost, LetsEncrypt
from subprocess import call
from free_tls_certificates import client
from django.utils import timezone
import requests.exceptions
import acme.messages
import uuid
import os

def issue_cert():
	for vhost in VHost.objects.filter(use_letsencrypt=True, letsencrypt__state__in=['REQUESTED', 'EXPIRE_SOON']):
		try:
			data = client.issue_certificate(
				[unicode(vhost),] + list(vhost.vhostalias_set.values_list('alias', flat=True)),
				settings.LETSENCRYPT_STATE_FOLDER,
				agree_to_tos_url = settings.LETSENCRYPT_TOS,
				acme_server = settings.LETSENCRYPT_ACME_SERVER)

			cert = SSLCert()
			cert.set_cert(cert=data['cert'], key=data['private_key'], ca=data['chain'])
			cert.save()

			vhost.cert = cert
			vhost.save()

			vhost.letsencrypt.state = 'VALID'
			vhost.letsencrypt.last_message = 'Certificate installed'
			vhost.letsencrypt.save()

		except client.NeedToTakeAction as e:
			for action in e.actions:
				if isinstance(action, client.NeedToInstallFile):
					vhost.letsencrypt.last_message = 'Domainname validation required.'
					vhost.letsencrypt.save()
					with open(settings.LETSENCRYPT_ACME_FOLDER + action.file_name, 'a') as f:
						f.write(action.contents)
		except client.WaitABit as e:
			vhost.letsencrypt.last_message = 'Retry later'
			vhost.letsencrypt.save()
		except Exception as e:
			vhost.letsencrypt.last_message = str(e)
			vhost.letsencrypt.save()

def set_expire_soon():
	for vhost in VHost.objects.filter(use_letsencrypt=True, cert__isnull=False, letsencrypt__state__in=['VALID', 'EXPIRE_SOON']):
		if vhost.cert.valid_not_after < (timezone.now() + timezone.timedelta(days=30)):
			vhost.letsencrypt.state = 'EXPIRE_SOON'
			vhost.letsencrypt.last_message = 'Certificate will expire at ' + str(vhost.cert.valid_not_after)
			vhost.letsencrypt.save()

class Command(BaseCommand):
	args = ''
	help = 'issue lets encrypt ssl certificates'

	def handle(self, *args, **options):
		set_expire_soon()
		issue_cert()
