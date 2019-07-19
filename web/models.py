from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from OpenSSL import SSL, crypto
from annoying.fields import AutoOneToOneField
from kumquat.models import Domain
from kumquat.utils import DomainNameValidator
from web.x509 import parseAsn1Generalizedtime, x509name_to_str, serial_to_hex
import re

default_length = 255

class VHost(models.Model):
	name   = models.CharField(max_length=default_length, verbose_name=_('Sub Domain'), help_text=_('Child part of your domain that is used to organize your site content.'), validators=[DomainNameValidator()])
	domain = models.ForeignKey(Domain, blank=False)
	cert   = models.ForeignKey('SSLCert', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='SSL Certificate')
	use_letsencrypt = models.BooleanField(verbose_name=_('SSL Certificate managed by Let\'s Encrypt'), default=False)

	def webroot(self):
		return settings.KUMQUAT_VHOST_ROOT + '/' + str(self.punycode())

	def __str__(self):
		return bytes(self.name, encoding="utf-8").decode("idna") + '.' + str(self.domain)

	def punycode(self):
		return str(self.name) + '.' + str(self.domain.punycode())

	def letsencrypt_state(self):
		if not self.use_letsencrypt:
			return 'NOT_USED'
		if not self.cert:
			return 'REQUEST'
		if self.cert.expire_soon():
			return 'RENEW'
		return 'VALID'

	def save(self, **kwargs):
		self.name = self.name.encode("idna")
		super(VHost, self).save(**kwargs)

	class Meta:
		unique_together = (("name", "domain"),)


class DefaultVHost(models.Model):
	domain = models.OneToOneField(Domain, primary_key=True)
	vhost  = models.ForeignKey(VHost, blank=False)

class VHostAlias(models.Model):
	alias  = models.CharField(max_length=default_length, verbose_name=_('Alias'), help_text=_('Server alias for virtual host.'), validators=[DomainNameValidator()], unique=True)
	vhost  = models.ForeignKey(VHost, blank=False)

	def __str__(self):
		return bytes(self.alias, encoding="utf-8").decode("idna")

	def punycode(self):
		return str(self.alias)

	def save(self, **kwargs):
		self.alias = self.alias.encode("idna")
		super(VHostAlias, self).save(**kwargs)


class LetsEncrypt(models.Model):
	vhost = AutoOneToOneField(VHost, on_delete=models.CASCADE)
	last_message = models.TextField(blank=True)

class SSLCert(models.Model):
	cn               = models.CharField(max_length=default_length)
	serial           = models.CharField(max_length=default_length)
	valid_not_before = models.DateTimeField()
	valid_not_after  = models.DateTimeField()
	subject          = models.CharField(max_length=default_length)
	issuer           = models.CharField(max_length=default_length)
	cert             = models.TextField()
	key              = models.TextField()
	ca               = models.TextField()


	def set_cert(self, cert, key, ca):
		self.cert = cert
		self.key  = key
		self.ca   = ca

		cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

		self.subject = x509name_to_str(cert.get_subject())
		self.issuer  = x509name_to_str(cert.get_issuer())
		self.cn      = cert.get_subject().commonName
		self.serial  = serial_to_hex(cert.get_serial_number())
		self.valid_not_before = parseAsn1Generalizedtime(cert.get_notBefore())
		self.valid_not_after  = parseAsn1Generalizedtime(cert.get_notAfter())

	def bundle_name(self):
		"returns a string that could be used as filename"
		fname = str(self.pk) + '-' + re.sub(r"[^a-z._-]", "", self.cn.lower()) + '.pem'
		return settings.KUMQUAT_CERT_PATH + '/' + fname

	def write_bundle(self):
		with open(self.bundle_name(), "w") as f:
			f.write(self.cert)
			f.write(self.key)
			f.write(self.ca)

	def expire_soon(self):
		return self.valid_not_after < (timezone.now() + timezone.timedelta(days=30))

	def __str__(self):
		return self.cn + ' (' + self.serial + ')'
