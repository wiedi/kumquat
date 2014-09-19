from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_unicode
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class DomainNameValidator(RegexValidator):
	# from URLValidator + there can be most 127 labels (at most 255 total chars)
	regex = re.compile(
		r'^(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.){0,126}(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))$',
		re.IGNORECASE
		)
	message = 'Enter a valid domain name value'

	def __init__(self, *args, **kwargs):
		self.accept_idna = bool(kwargs.pop('accept_idna', True))
		super(DomainNameValidator, self).__init__(*args, **kwargs)
		if self.accept_idna:
			self.message = 'Enter a valid plain or internationalized domain name value'

	def __call__(self, value):
		# validate
		try:
			super(DomainNameValidator, self).__call__(value)
		except ValidationError as e:
			# maybe this is a unicode-encoded IDNA string?
			if not self.accept_idna: raise
			if not value: raise
			# convert it unicode -> ascii
			try:
				asciival = smart_unicode(value).encode('idna')
			except UnicodeError:
				raise e # raise the original ASCII error
			# validate the ascii encoding of it
			super(DomainNameValidator, self).__call__(asciival)
