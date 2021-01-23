from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _
from kumquat.utils import LoginRequiredMixin, SuccessActionFormMixin, SuccessActionDeleteMixin
from cron.models import Cronjob


def update_cronjobs(*args, **kwargs):
	if not settings.KUMQUAT_USE_0RPC:
		return
	import zerorpc
	zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET).update_cronjobs()

class CronjobList(LoginRequiredMixin, ListView):
	model = Cronjob

class CronjobCreate(LoginRequiredMixin, SuccessActionFormMixin, SuccessMessageMixin, CreateView):
	model = Cronjob
	fields = ('command','when',)
	success_url = reverse_lazy('cronjob_list')
	success_message = _("Cronjob was created successfully")
	success_action = update_cronjobs

class CronjobUpdate(LoginRequiredMixin, SuccessActionFormMixin, SuccessMessageMixin, UpdateView):
	model = Cronjob
	fields = ('command','when',)
	success_url = reverse_lazy('cronjob_list')
	success_message = _("Cronjob was updated successfully")
	success_action = update_cronjobs

class CronjobDelete(LoginRequiredMixin, SuccessActionDeleteMixin, DeleteView):
	model = Cronjob
	success_url = reverse_lazy('cronjob_list')
	success_action = update_cronjobs
