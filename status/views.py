from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from info import info

@login_required
def status(request):
	return render(request, 'status/status.html', {'info': info()})