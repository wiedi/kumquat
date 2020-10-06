from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q
from django.template.loader import render_to_string
from django.conf import settings
from web.models import SSLCert, VHost, LetsEncrypt
from subprocess import call
from django.utils import timezone
from cProfile import Profile
import requests.exceptions
import uuid
import os
import io
import pstats
import re
import sys

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import josepy as jose
import OpenSSL

from acme import challenges
from acme import client
from acme import crypto_util
from acme import errors
from acme import messages

if settings.KUMQUAT_USE_0RPC:
	import zerorpc

# Generate an account or receive the registration data required to order
# certificates via ACMEv2. If local account files already exists, do not
# generate a new account.
def account():
	# Store account information in an JWKRSA formated json file
	reg_file = settings.LETSENCRYPT_STATE_FOLDER + '/regr.json'
	key_file = settings.LETSENCRYPT_STATE_FOLDER + '/private_key.json'
	try:
		# Read existing account data and private key
		with open(reg_file, 'r') as f:
			regr = messages.RegistrationResource.json_loads(f.read())
		with open(key_file, 'r') as f:
			key  = jose.JWK.json_loads(f.read())
	except IOError as error:
		# Generate new private key, as we expect that the account doesn't exist
		private_key = rsa.generate_private_key(
			public_exponent = 65537,
			key_size        = settings.LETSENCRYPT_ACCT_KEY_BITS,
			backend         = default_backend()
		)
		key = jose.JWKRSA(key=private_key)
		# Prepare ACME client connection with account private key
		net         = client.ClientNetwork(key)
		directory   = messages.Directory.from_json(
			net.get(settings.LETSENCRYPT_ACME_SERVER).json()
		)
		client_acme = client.ClientV2(directory, net=net)
		# Generate a new account and store account information locally
		email = getattr(settings, 'KUMQUAT_EMAIL', None)
		regr  = client_acme.new_account(
			messages.NewRegistration.from_data(
				email                   = email,
				terms_of_service_agreed = True
			)
		)
		# Store private key as json format
		with open(key_file, 'w') as f:
			f.write(key.json_dumps())
		# Store regr information as json format
		with open(reg_file, 'w') as f:
			f.write(regr.json_dumps())

	return key, regr

def gen_csr(domain_names, pkey_pem=None):
	if pkey_pem is None:
		pkey = OpenSSL.crypto.PKey()
		pkey.generate_key(OpenSSL.crypto.TYPE_RSA, settings.LETSENCRYPT_CERT_KEY_BITS)
		pkey_pem = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, pkey)

	# Generate CSR based on the domains
	csr_pem = crypto_util.make_csr(pkey_pem, domain_names)
	return pkey_pem, csr_pem

def challenge_body(new_order):
	"""Extract authorization resource from within order resource."""
	# Authorization Resource: authz.
	# This object holds the offered challenges by the server and their status.
	authz_list = new_order.authorizations
	challenge = []

	for authz in authz_list:
		# Choosing challenge.
		# authz.body.challenges is a set of ChallengeBody objects.
		for i in authz.body.challenges:
			# Find the supported challenge.
			if isinstance(i.chall, challenges.HTTP01):
				challenge += [i]
	return challenge

	raise Exception('HTTP-01 challenge was not offered by the CA server.')

def split_fullchain(fullchain_pem):
	re_pem         = b"(-+BEGIN (?:.+)-+[\\r\\n]+(?:[A-Za-z0-9+/=]{1,64}[\\r\\n]+)+-+END (?:.+)-+[\\r\\n]+)"
	cert, ca       = re.findall(re_pem, str.encode(fullchain_pem))
	return cert.decode("ascii"), ca.decode("ascii")

def issue_cert():
	# Use or generate new account for ACME API
	key, regr = account()

	vhosts = [vhost for vhost in VHost.objects.filter(use_letsencrypt=True) if vhost.letsencrypt_state() in ['REQUEST', 'RENEW']]
	if not vhosts:
		return

	try:
		net = client.ClientNetwork(key = key, account = regr)
		directory = messages.Directory.from_json(net.get(settings.LETSENCRYPT_ACME_SERVER).json())
		client_acme = client.ClientV2(directory, net=net)
	except Exception as e:
		sys.stderr.write("Connection issues to " + str(settings.LETSENCRYPT_ACME_SERVER) + "\n")
		sys.stderr.write("Verify current Let's Encrypt status via https://letsencrypt.status.io/\n")
		sys.exit(1)

	letsencrypt_issued = False
	for vhost in vhosts:
		pkey_pem = None
		if vhost.letsencrypt_state() is 'RENEW':
			pkey_pem = vhost.cert.key

		# Generate a certificate request based on the vhost and aliases.
		pkey_pem, csr_pem = gen_csr([str(vhost.punycode()),] + [vhostalias.punycode() for vhostalias in vhost.vhostalias_set.all()], pkey_pem)

		# Create new certificate order
		challbs = []
		try:
			new_order = client_acme.new_order(csr_pem)
			challbs  += challenge_body(new_order)
		except Exception as e:
			vhost.letsencrypt.last_message = str(e)
			vhost.letsencrypt.save()
			continue

		# Write tokens for validation for each vhost and alias
		for challb in challbs:
			# Write well known data
			token      = challb.path.rsplit('/', 1)[1]
			validation = challb.validation(key)
			path       = os.path.join(settings.LETSENCRYPT_ACME_FOLDER, token)
			with open(path, 'w') as validation_file:
				validation_file.write(validation)

			# Poll authorizations and finalize the order
			response, validation = challb.response_and_validation(client_acme.net.key)
			client_acme.answer_challenge(challb, response)
	
		# Finalize the order
		# Default Timeout after 90 seconds
		try:
			finalized_order = client_acme.poll_and_finalize(new_order)
			server_cert, ca = split_fullchain(finalized_order.fullchain_pem)

			cert = SSLCert()
			cert.set_cert(cert=server_cert, key=pkey_pem, ca=ca)
			cert.save()

			vhost.cert = cert
			vhost.save()

			vhost.letsencrypt.last_message = ''
			vhost.letsencrypt.save()

			# Delete the token file when the authentication was successful
			os.remove(path)

			letsencrypt_issued = True
		except errors.TimeoutError as e:
			vhost.letsencrypt.last_message = 'Error when polling an authorization or an order times out!'
			vhost.letsencrypt.save()
		except errors.ValidationError as e:
			vhost.letsencrypt.last_message = ''
			for rs in e.failed_authzrs:
				for challenge in rs.body.challenges:
					vhost.letsencrypt.last_message += str(challenge.error.detail)
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
