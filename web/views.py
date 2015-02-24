from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from datetime import datetime
from kumquat.utils import LoginRequiredMixin
from models import VHost, SSLCert, DefaultVHost
from forms import SSLCertForm, SnapshotForm
import zerorpc

# VHost

class VHostList(LoginRequiredMixin, ListView):
	model = VHost

class VHostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = VHost
	success_url = reverse_lazy('web_vhost_list')
	success_message = _("%(name)s was created successfully")

class VHostUpdate(LoginRequiredMixin, UpdateView):
	model = VHost
	#form_class = AccountUpdateForm
	fields = ['cert']
	success_url = reverse_lazy('web_vhost_list')

class VHostDelete(LoginRequiredMixin, DeleteView):
	model = VHost
	success_url = reverse_lazy('web_vhost_list')


# Default VHost

@require_POST
@login_required
def vhostCatchallSet(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	DefaultVHost(vhost = v, domain = v.domain).save()
	return redirect('web_vhost_list')

@require_POST
@login_required
def vhostCatchallDelete(request, pk):
	get_object_or_404(DefaultVHost, pk = pk).delete()
	return redirect('web_vhost_list')


# SSL Certs

class SSLCertList(LoginRequiredMixin, ListView):
	model = SSLCert

@login_required
def sslcertCreate(request):
	form = SSLCertForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		c = SSLCert()
		c.set_cert(request.FILES['cert'].read(), request.FILES['key'].read(), request.FILES['ca'].read())
		c.save()
		messages.success(request, _("Successfull added"))
		return redirect('web_sslcert_list')
	return render(request, 'web/sslcert_form.html', {'form': form})

class SSLCertDelete(LoginRequiredMixin, DeleteView):
	model = SSLCert
	success_url = reverse_lazy('web_sslcert_list')

# Snapshots

@login_required
def vhostSnapshotList(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
	snapshots = z.snapshot_list(v.pk)
	for i, s in enumerate(snapshots):
		snapshots[i]['creation'] = datetime.fromtimestamp(snapshots[i]['creation'])

	return render(request, 'web/snapshot_list.html', {'vhost': v, 'object_list': snapshots})


@login_required
def vhostSnapshotCreate(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	form = SnapshotForm(request.POST or None)
	if form.is_valid():
		z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
		if z.snapshot_create(v.pk, form.cleaned_data.get("name")):
			messages.success(request, _("Snapshot created"))
		else:
			messages.error(request, _("Snapshot not created"))
		return redirect('web_vhost_snapshot_list', pk)
	return render(request, 'web/snapshot_form.html', {'form': form})


@require_POST
@login_required
def vhostSnapshotRollback(request, pk, name):
	v = get_object_or_404(VHost, pk = pk)
	z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
	z.snapshot_rollback(v.pk, name)
	return redirect('web_vhost_snapshot_list', pk)


@require_POST
@login_required
def vhostSnapshotDelete(request, pk, name):
	v = get_object_or_404(VHost, pk = pk)
	z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
	z.snapshot_delete(v.pk, name)
	return redirect('web_vhost_snapshot_list', pk)
