from django.db import models
from OpenSSL import SSL, crypto
from x509 import parseAsn1Generalizedtime, x509name_to_str

default_length = 255

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
		self.serial  = cert.get_serial_number()
		self.valid_not_before = parseAsn1Generalizedtime(cert.get_notBefore())
		self.valid_not_after  = parseAsn1Generalizedtime(cert.get_notAfter())

	def __unicode__(self):
		return self.cn + ' (' + self.serial + ')'
