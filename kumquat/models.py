from django.db import models
from django.utils.translation import ugettext_lazy as _

class Domain(models.Model):
	name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'), help_text=_('Your primary domain (example.com) that you like to use for the different services.'))

	def __unicode__(self):
		return self.name
