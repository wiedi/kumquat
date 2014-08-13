from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.http import Http404
from kumquat.utils import LoginRequiredMixin
from forms import *

def list_databases(*kwargs):
		cursor = connections['kumquat_mysql'].cursor()
		cursor.execute("SHOW DATABASES LIKE 'db_%'")
		dbs = []
		for db in cursor.fetchall():
			database = db[0]
			name = database[3:]
			dbs += [{
				"name": name,
				"database": database,
			}]
		return dbs


class DatabaseList(LoginRequiredMixin, ListView):
	template_name = 'mysql/database_list.html'
	get_queryset  = list_databases

class DatabaseCreate(LoginRequiredMixin, FormView):
	template_name = 'mysql/database_form.html'
	success_url   = reverse_lazy('mysql_database_list')
	form_class    = DatabaseCreateForm

	def form_valid(self, form):
		form.create_database()
		return super(DatabaseCreate, self).form_valid(form)

@login_required
def databaseUpdate(request, slug):
	dbs = [db["name"] for db in list_databases()]
	if(slug not in dbs):
		raise Http404
	form = DatabaseUpdateForm(request.POST or None)
	if form.is_valid():
		form.update_database(slug)
		return redirect('mysql_database_list')
	return render(request, 'mysql/database_password.html', {'form': form})


@login_required
def databaseDelete(request, slug):
	dbs = [db["name"] for db in list_databases()]
	if(slug not in dbs):
		raise Http404
	if request.method != "POST":
		raise PermissionDenied
		
	database = dbname(slug)
	c = connections['kumquat_mysql'].cursor()
	c.execute("drop user " + slug)
	c.execute("drop database " + database)
	return redirect('mysql_database_list')
