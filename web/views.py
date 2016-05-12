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
from kumquat.utils import LoginRequiredMixin, SuccessActionFormMixin, SuccessActionDeleteMixin
from models import VHost, SSLCert, DefaultVHost
from forms import SSLCertForm, SnapshotForm
import zerorpc
import mmap
import os

def update_vhosts(*args, **kwargs):
	zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET).update_vhosts()

def tail(filename, n):
	# Returns last n lines from the filename. No exception handling
	size = os.path.getsize(filename)
	with open(filename, "rb") as f:
		fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
		try:
			for i in xrange(size - 1, -1, -1):
				if fm[i] == '\n':
					n -= 1
					if n == -1:
						break
			return fm[i + 1 if i else 0:].splitlines()
		finally:
			fm.close()


# VHost

class VHostList(LoginRequiredMixin, ListView):
	model = VHost

class VHostCreate(LoginRequiredMixin, SuccessMessageMixin, SuccessActionFormMixin, CreateView):
	model = VHost
	fields = ('name', 'domain', 'cert')
	success_url = reverse_lazy('web_vhost_list')
	success_message = _("%(name)s was created successfully")
	success_action = update_vhosts

class VHostUpdate(LoginRequiredMixin, SuccessActionFormMixin, UpdateView):
	model = VHost
	fields = ['cert']
	success_url = reverse_lazy('web_vhost_list')
	success_action = update_vhosts

class VHostDelete(LoginRequiredMixin, SuccessActionDeleteMixin, DeleteView):
	model = VHost
	success_url = reverse_lazy('web_vhost_list')
	success_action = update_vhosts

# Default VHost

@require_POST
@login_required
def vhostCatchallSet(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	DefaultVHost(vhost = v, domain = v.domain).save()
	update_vhosts()
	return redirect('web_vhost_list')

@require_POST
@login_required
def vhostCatchallDelete(request, pk):
	get_object_or_404(DefaultVHost, pk = pk).delete()
	update_vhosts()
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


# Error Logs

@login_required
def vhostErrorLogList(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	elogfile = settings.KUMQUAT_VHOST_ERROR_LOG.format(vhost = unicode(v))
	try:
		errorlog = [s.replace('\\n', '\n').strip() for s in tail(elogfile, 25)]
	except:
		errorlog = []



	return render(request, 'web/vhost_errorlog.html', {'errorlog': errorlog})

