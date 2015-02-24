from django import forms
from django.utils.translation import ugettext_lazy as _
from OpenSSL import SSL, crypto

class SSLCertForm(forms.Form):
	cert = forms.FileField(label = _("Certificate"))
	key  = forms.FileField(label = _("Privatekey"))
	ca   = forms.FileField(label = _("Certificate Authority"))

	def clean(self):
		cleaned_data = self.cleaned_data
		try:
			cert = cleaned_data.get('cert').read()
			key  = cleaned_data.get('key').read()
			ca   = cleaned_data.get('ca').read()

			cleaned_data.get('cert').seek(0)
			cleaned_data.get('key').seek(0)
			cleaned_data.get('ca').seek(0)

			cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
			key  = crypto.load_privatekey(crypto.FILETYPE_PEM, key)

			# check if keypair matches
			ctx = SSL.Context(SSL.SSLv23_METHOD)
			ctx.use_certificate(cert)
			ctx.use_privatekey(key)
			ctx.check_privatekey()
		except:
			raise forms.ValidationError(_("Please upload a matching key-pair in PEM format."))

		return cleaned_data


class SnapshotForm(forms.Form):
	name     = forms.RegexField(max_length=16, regex=r'^[a-z0-9_-]+$', label = _("Name"))
