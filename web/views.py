from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from models import SSLCert
from forms import SSLCertForm

class SSLCertList(ListView):
	model = SSLCert

def sslcertCreate(request):
	form = SSLCertForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		c = SSLCert()
		c.set_cert(request.FILES['cert'].read(), request.FILES['key'].read(), request.FILES['ca'].read())
		c.save()
		return redirect('web_sslcert_list')
	return render(request, 'web/sslcert_form.html', {'form': form})

class SSLCertDelete(DeleteView):
	model = SSLCert
	success_url = reverse_lazy('web_sslcert_list')