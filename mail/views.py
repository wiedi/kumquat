from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from kumquat.utils import LoginRequiredMixin
from kumquat.models import Domain
from mail.models import Account, Redirect
from mail.forms import AccountUpdateForm, AccountCreateForm
import json
import re

# Accounts

class AccountList(LoginRequiredMixin, ListView):
	model = Account

class AccountCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Account
	form_class = AccountCreateForm
	success_url = reverse_lazy('mail_account_list')
	success_message = _("%(name)s was created successfully")
	
	def form_valid(self, form):
		password = form.cleaned_data.get('password')
		self.object = form.save(commit=False)
		self.object.set_password(password)
		self.object.save()
		return super().form_valid(form)


class AccountUpdate(LoginRequiredMixin, UpdateView):
	model = Account
	form_class = AccountUpdateForm
	success_url = reverse_lazy('mail_account_list')
	
	def form_valid(self, form):
		new_password = form.cleaned_data.get('new_password')
		if new_password:
			self.object = form.save(commit=False)
			self.object.set_password(new_password)
			self.object.save()
		return super().form_valid(form)


class AccountDelete(LoginRequiredMixin, DeleteView):
	model = Account
	success_url = reverse_lazy('mail_account_list')

# Redirects

class RedirectList(LoginRequiredMixin, ListView):
	model = Redirect

class RedirectCreate(LoginRequiredMixin, CreateView):
	model = Redirect
	fields = ('name', 'domain', 'to')
	success_url = reverse_lazy('mail_redirect_list')
	success_message = _("%(name)s was created successfully")

class RedirectUpdate(LoginRequiredMixin, UpdateView):
	model = Redirect
	fields = ['to']
	success_url = reverse_lazy('mail_redirect_list')

class RedirectDelete(LoginRequiredMixin, DeleteView):
	model = Redirect
	success_url = reverse_lazy('mail_redirect_list')


# core.io json export

def export(request):
	if request.GET.get('token', False) != settings.CORE_MAIL_TOKEN:
		raise PermissionDenied
	
	data = {}
	for domain in Domain.objects.all():
		punycode_domain = domain.punycode()
		data[punycode_domain] = {
			"account": [],
			"alias":   [],
		}
		for account in domain.mail_accounts.all():
			spoofing_whitelist = getattr(settings, 'CORE_MAIL_WHITELIST', None)
			if spoofing_whitelist == None:
				spoofing_whitelist = punycode_domain
			data[punycode_domain]["account"] += [{
				"name":                 account.name,
				"password":             account.password,
				"spoofing_whitelist":   spoofing_whitelist,
				"subaddress_extension": account.subaddress,
			}]
		for redirect in domain.redirect_set.all():
			to = ",".join(re.sub("[\n,\s]", " ", redirect.to).split())
			data[punycode_domain]["alias"] += [{
				"name": redirect.name,
				"to":   to,
			}]

	return HttpResponse(json.dumps(data), content_type='application/json')
