from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Account
from forms import AccountUpdateForm

class AccountList(ListView):
	model = Account

class AccountCreate(CreateView):
	model = Account
	success_url = reverse_lazy('ftp_account_list')
	
	def form_valid(self, form):
		password = form.cleaned_data.get('password')
		self.object = form.save(commit=False)
		self.object.set_password(password)
		self.object.save()
		return super(AccountCreate, self).form_valid(form)


class AccountUpdate(UpdateView):
	model = Account
	form_class = AccountUpdateForm
	success_url = reverse_lazy('ftp_account_list')
	
	def form_valid(self, form):
		new_password = form.cleaned_data.get('new_password')
		if new_password:
			self.object = form.save(commit=False)
			self.object.set_password(new_password)
			self.object.save()
		return super(AccountUpdate, self).form_valid(form)


class AccountDelete(DeleteView):
	model = Account
	success_url = reverse_lazy('ftp_account_list')