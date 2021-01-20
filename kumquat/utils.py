from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_text
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

class SuccessActionFormMixin(object):
	def success_action(self):
		pass

	def form_valid(self, form):
		ret = super().form_valid(form)
		self.success_action()
		return ret

class SuccessActionDeleteMixin(object):
	def success_action(self):
		pass

	def delete(self, request, *args, **kwargs):
		ret = super().delete(request, *args, **kwargs)
		# this is a lie, we can't be sure the delte was successful
		self.success_action()
		return ret


class DomainNameValidator(RegexValidator):
	# from URLValidator + there can be most 127 labels (at most 255 total chars)
	regex = re.compile(
		r'^(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.){0,126}(?:[A-Z]{1,6}\.?|[A-Z0-9-]{2,}\.?))$',
		re.IGNORECASE
		)
	message = 'Enter a valid domain name value'

	def __init__(self, *args, **kwargs):
		self.accept_idna = bool(kwargs.pop('accept_idna', True))
		super().__init__(*args, **kwargs)
		if self.accept_idna:
			self.message = 'Enter a valid plain or internationalized domain name value'

	def __call__(self, value):
		# validate
		try:
			super().__call__(value)
		except ValidationError as e:
			# maybe this is a unicode-encoded IDNA string?
			if not self.accept_idna: raise
			if not value: raise
			# convert it unicode -> ascii
			try:
				asciival = smart_text(value).encode('idna').decode('ascii')
			except UnicodeError:
				raise e # raise the original ASCII error
			# validate the ascii encoding of it
			super().__call__(asciival)
