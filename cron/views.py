from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from kumquat.utils import LoginRequiredMixin, SuccessActionFormMixin, SuccessActionDeleteMixin
from models import Cronjob

class CronjobList(LoginRequiredMixin, ListView):
    model = Cronjob

class CronjobCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cronjob
    fields = ('command','when',)
    success_url = reverse_lazy('cronjob_list')
    success_message = _("Cronjob was created successfully")

class CronjobUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cronjob
    fields = ('command','when',)
    success_url = reverse_lazy('cronjob_list')
    success_message = _("Cronjob was updated successfully")

class CronjobDelete(LoginRequiredMixin, DeleteView):
    model = Cronjob
    success_url = reverse_lazy('cronjob_list')
