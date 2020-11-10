from django.db import models
from django.utils.translation import ugettext_lazy as _
from passlib.hash import sha512_crypt
from kumquat.models import Domain

default_length = 255

class Account(models.Model):
	name       = models.CharField(max_length=default_length)
	domain     = models.ForeignKey(Domain, related_name='mail_accounts', on_delete=models.CASCADE)
	password   = models.CharField(max_length=default_length)
	subaddress = models.BooleanField(verbose_name=_('Subaddress extension'), help_text=_('Enable subaddress extension (e.g. primary+sub@example.com'), default=False)

	def set_password(self, password):
		self.password = sha512_crypt.encrypt(password)

	def __str__(self):
		return str(self.name) + '@' + str(self.domain)

	def save(self, **kwargs):
		self.name = self.name.lower()
		super().save(**kwargs)

	class Meta:
		unique_together = (('name', 'domain'),)


class Redirect(models.Model):
	name   = models.CharField(max_length=default_length)
	domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
	to     = models.TextField()

	def __str__(self):
		return self.name + '@' + str(self.domain)

	def save(self, **kwargs):
		self.name = self.name.lower()
		self.to   = self.to.lower()
		super().save(**kwargs)

	class Meta:
		unique_together = (('name', 'domain'),)

