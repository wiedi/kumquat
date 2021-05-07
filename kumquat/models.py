from django.db import models
from django.utils.translation import ugettext_lazy as _
from kumquat.utils import DomainNameValidator

class Domain(models.Model):
	name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'), help_text=_('Your primary domain (example.com) that you like to use for the different services.'), validators=[DomainNameValidator()])

	def __str__(self):
		return self.name.encode().decode("idna")

	def punycode(self):
		return self.name

	def save(self, **kwargs):
		self.name = self.name.encode("idna").decode().lower()
		super().save(**kwargs)
