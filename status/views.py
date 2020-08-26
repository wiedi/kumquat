from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from status.info import info
from web.models import LetsEncrypt, SSLCert

@login_required
def status(request):
	le_info = LetsEncrypt.objects.exclude(last_message__isnull=True).exclude(last_message__exact='')
	return render(request, 'status/status.html', {'info': info(), 'le_info': le_info})
