from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import connections, transaction

def dbname(username):
	return 'db_' + username

class DatabaseCreateForm(forms.Form):
	name     = forms.RegexField(max_length=16, regex=r'^[a-z0-9_]+$', label = _("Name"))
	password = forms.CharField(widget=forms.widgets.PasswordInput, label = _("Password"))
	
	def clean(self):
		cleaned_data = super().clean()

		name = cleaned_data.get("name")
		if not name:
			raise forms.ValidationError("Name invalid")

		database = dbname(name)
		cursor   = connections['kumquat_mysql'].cursor()

		cursor.execute('SHOW DATABASES LIKE %s', [database])
		if cursor.rowcount > 0:
			 raise forms.ValidationError("Databse name already in use")

		cursor.execute('SELECT user FROM mysql.user WHERE user = %s', [name])
		if cursor.rowcount > 0:
			 raise forms.ValidationError("Username already in use")

		return cleaned_data
	
	def create_database(self):
		name     = self.cleaned_data.get("name")
		password = self.cleaned_data.get("password")
		database = dbname(name)

		c = connections['kumquat_mysql'].cursor()
		with transaction.atomic(using='kumquat_mysql'):
			# we can concat the database name with the query because only safe characters are allowed by the regex field
			c.execute('CREATE DATABASE ' + database)
			# clear possible previous permissions
			c.execute("DROP USER IF EXISTS %s@'%%'",        [name])
			c.execute("DROP USER IF EXISTS %s@'localhost'", [name])
			c.execute("CREATE USER %s@'%%'        IDENTIFIED BY %s PASSWORD EXPIRE NEVER", [name, password])
			c.execute("CREATE USER %s@'localhost' IDENTIFIED BY %s PASSWORD EXPIRE NEVER", [name, password])
			c.execute("GRANT ALL ON " + database + ".* TO %s@'%%' ", [name])
			c.execute("GRANT ALL ON " + database + ".* TO %s@'localhost'", [name])

class DatabaseUpdateForm(forms.Form):
	new_password = forms.CharField(widget=forms.widgets.PasswordInput, label = _("Password"))

	def update_database(self, name):
		password = self.cleaned_data.get("new_password")
		c = connections['kumquat_mysql'].cursor()
		with transaction.atomic(using='kumquat_mysql'):
			c.execute("ALTER USER %s@'%%'        IDENTIFIED BY %s PASSWORD EXPIRE NEVER", [name, password])
			c.execute("ALTER USER %s@'localhost' IDENTIFIED BY %s PASSWORD EXPIRE NEVER", [name, password])
