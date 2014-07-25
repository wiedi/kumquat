from django.shortcuts import render
from info import info

def status(request):
	return render(request, 'status/status.html', {'info': info()})