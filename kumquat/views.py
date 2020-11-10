from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from kumquat.models import Domain
from kumquat.utils import LoginRequiredMixin

class DomainList(LoginRequiredMixin, ListView):
	model = Domain

class DomainCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Domain
	fields = ('name',)
	success_url = reverse_lazy('domain_list')
	success_message = _("%(name)s was created successfully")

class DomainDelete(LoginRequiredMixin, DeleteView):
	model = Domain
	success_url = reverse_lazy('domain_list')
