from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.timezone import now
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from datetime import datetime
from kumquat.utils import LoginRequiredMixin, SuccessActionFormMixin, SuccessActionDeleteMixin
from web.models import VHost, SSLCert, DefaultVHost, VHostAlias
from web.forms import SSLCertForm, SnapshotForm, VHostAliasForm
if settings.KUMQUAT_USE_0RPC:
	import zerorpc
import mmap
import os
import re

def update_vhosts(*args, **kwargs):
	if not settings.KUMQUAT_USE_0RPC:
		return
	zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET).update_vhosts()

def tail(filename, n):
	# Returns last n lines from the filename. No exception handling
	size = os.path.getsize(filename)
	with open(filename, "rb") as f:
		fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
		try:
			for i in range(size - 1, -1, -1):
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
	fields = ('name', 'domain', 'cert', 'use_letsencrypt')
	success_url = reverse_lazy('web_vhost_list')
	success_message = _("%(name)s was created successfully")
	success_action = update_vhosts

class VHostUpdate(LoginRequiredMixin, SuccessActionFormMixin, UpdateView):
	model = VHost
	fields = ['cert', 'use_letsencrypt']
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

# VHost Alias

@login_required
def vhostAliasList(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	return render(request, 'web/vhostalias_list.html', {'vhost': v, 'object_list': VHostAlias.objects.filter(vhost = pk)})

@login_required
def vhostAliasAdd(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	form = VHostAliasForm(request.POST or None)
	if form.is_valid():
		alias = form.save(commit=False)
		alias.vhost = v
		alias.save()
		update_vhosts()
		messages.success(request, _("Successfull added"))
		return redirect('web_vhost_alias_list', v.pk)
	return render(request, 'web/vhostalias_form.html', {'form': form})

@require_POST
@login_required
def vhostAliasDelete(request, pk):
	alias = get_object_or_404(VHostAlias, pk = pk)
	vhost = alias.vhost
	alias.delete()
	update_vhosts()
	return redirect('web_vhost_alias_list', vhost.pk)

# SSL Certs

class SSLCertList(LoginRequiredMixin, ListView):
	model = SSLCert

	def get_queryset(self):
		return SSLCert.objects.filter(valid_not_after__gt = now())


class ExpiredSSLCertList(LoginRequiredMixin, ListView):
	model = SSLCert

	def get_queryset(self):
		return SSLCert.objects.filter(valid_not_after__lt = now())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['show_expired'] = True
		return context


@login_required
def sslcertCreate(request):
	form = SSLCertForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		c = SSLCert()
		c.set_cert(
			request.FILES['cert'].read().decode(),
			request.FILES['key'].read().decode(),
			request.FILES['ca'].read().decode()
		)
		c.save()
		messages.success(request, _("Successfull added"))
		return redirect('web_sslcert_list')
	return render(request, 'web/sslcert_form.html', {'form': form})

class SSLCertDelete(LoginRequiredMixin, DeleteView):
	model = SSLCert
	success_url = reverse_lazy('web_sslcert_list')

@login_required
@require_POST
def sslcertDeleteExpired(request):
	SSLCert.objects.filter(valid_not_after__lt = now()).delete()
	return redirect('web_sslcert_list')


# Snapshots

@login_required
def vhostSnapshotList(request, pk):
	if not settings.KUMQUAT_USE_0RPC:
		raise Http404
	v = get_object_or_404(VHost, pk = pk)
	z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
	snapshots = z.snapshot_list(v.pk)
	for i, s in enumerate(snapshots):
		snapshots[i]['creation'] = datetime.fromtimestamp(snapshots[i]['creation'])

	return render(request, 'web/snapshot_list.html', {'vhost': v, 'object_list': snapshots})


@login_required
def vhostSnapshotCreate(request, pk):
	if not settings.KUMQUAT_USE_0RPC:
		raise Http404
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
	if not settings.KUMQUAT_USE_0RPC:
		raise Http404
	v = get_object_or_404(VHost, pk = pk)
	z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
	z.snapshot_rollback(v.pk, name)
	return redirect('web_vhost_snapshot_list', pk)


@require_POST
@login_required
def vhostSnapshotDelete(request, pk, name):
	if not settings.KUMQUAT_USE_0RPC:
		raise Http404
	v = get_object_or_404(VHost, pk = pk)
	z = zerorpc.Client(connect_to=settings.KUMQUAT_BACKEND_SOCKET)
	z.snapshot_delete(v.pk, name)
	return redirect('web_vhost_snapshot_list', pk)


# Error Logs

@login_required
def vhostErrorLogList(request, pk):
	v = get_object_or_404(VHost, pk = pk)
	elogfile = settings.KUMQUAT_VHOST_ERROR_LOG.format(vhost = str(v))
	try:
		errorlog = tail(elogfile, 25)
	except:
		errorlog = []

	log = []
	for line in errorlog:
		m = re.match(r"\[(?P<time>[^\]]+)\] \[(?P<module>[^\]]+)\] \[pid (?P<pid>\d+):tid (?P<tid>\d+)\] \[client (?P<client>[^\]]+)\] (?P<message>.+)", line.decode())
		if not m: continue
		s = m.groupdict()
		s['message'] = s['message'].replace('\\n', '\n').strip()
		log += [s]

	return render(request, 'web/vhost_errorlog.html', {'vhost': v, 'log': log})

