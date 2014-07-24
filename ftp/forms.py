from django import forms
from models import Account

class AccountUpdateForm(forms.ModelForm):
	new_password = forms.CharField(required=False, widget=forms.widgets.PasswordInput)
	class Meta:
		model = Account
		fields = ('domain', 'path')

