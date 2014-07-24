from django.db import models
from django.utils.translation import ugettext_lazy as _
from passlib.hash import sha512_crypt
from kumquat.models import Domain

default_length = 255

class Account(models.Model):
	name     = models.CharField(max_length=default_length, unique=True)
	password = models.CharField(max_length=default_length)
	domain   = models.ForeignKey(Domain)
	path     = models.CharField(max_length=default_length, default="/")

	def set_password(self, password):
		self.password = sha512_crypt.encrypt(password)

	def __unicode__(self):
		return self.name