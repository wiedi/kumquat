from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Domain

class DomainList(ListView):
    model = Domain

class DomainCreate(CreateView):
    model = Domain
    success_url = reverse_lazy('domain_list')

class DomainDelete(DeleteView):
    model = Domain
    success_url = reverse_lazy('domain_list')