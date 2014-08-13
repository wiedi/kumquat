from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Domain
from utils import LoginRequiredMixin

class DomainList(LoginRequiredMixin, ListView):
    model = Domain

class DomainCreate(LoginRequiredMixin, CreateView):
    model = Domain
    success_url = reverse_lazy('domain_list')

class DomainDelete(LoginRequiredMixin, DeleteView):
    model = Domain
    success_url = reverse_lazy('domain_list')