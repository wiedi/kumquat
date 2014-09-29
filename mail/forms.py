from django import forms
from models import Account

class AccountCreateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.widgets.PasswordInput)
	class Meta:
		model = Account

class AccountUpdateForm(forms.ModelForm):
	new_password = forms.CharField(required=False, widget=forms.widgets.PasswordInput)
	class Meta:
		model = Account
		fields = ()

