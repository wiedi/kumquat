from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from kumquat.utils import LoginRequiredMixin
from ftp.models import Account
from ftp.forms import AccountUpdateForm, AccountCreateForm

class AccountList(LoginRequiredMixin, ListView):
	model = Account

class AccountCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Account
	form_class = AccountCreateForm
	success_url = reverse_lazy('ftp_account_list')
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
	success_url = reverse_lazy('ftp_account_list')
	
	def form_valid(self, form):
		new_password = form.cleaned_data.get('new_password')
		if new_password:
			self.object = form.save(commit=False)
			self.object.set_password(new_password)
			self.object.save()
		return super().form_valid(form)


class AccountDelete(LoginRequiredMixin, DeleteView):
	model = Account
	success_url = reverse_lazy('ftp_account_list')
