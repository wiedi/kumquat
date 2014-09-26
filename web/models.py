from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from OpenSSL import SSL, crypto
from x509 import parseAsn1Generalizedtime, x509name_to_str, serial_to_hex
from kumquat.models import Domain
from kumquat.utils import DomainNameValidator
import re

default_length = 255

class VHost(models.Model):
	name   = models.CharField(max_length=default_length, verbose_name=_('Sub Domain'), help_text=_('Child part of your domain that is used to organize your site content.'), validators=[DomainNameValidator()])
	domain = models.ForeignKey(Domain, blank=False)
	cert   = models.ForeignKey('SSLCert', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='SSL Certificate')

	def webroot(self):
		return settings.KUMQUAT_VHOST_ROOT + '/' + str(self)

	def __unicode__(self):
		return unicode(self.name) + '.' + unicode(self.domain)

	class Meta:
		unique_together = (("name", "domain"),)


class DefaultVHost(models.Model):
	domain = models.OneToOneField(Domain, primary_key=True)
	vhost  = models.ForeignKey(VHost, blank=False)


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

	def __unicode__(self):
		return self.cn + ' (' + self.serial + ')'
