from django import forms
from models import Account
from web.models import VHost

class AccountCreateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.widgets.PasswordInput)
	vhost    = forms.ModelChoiceField(queryset=VHost.objects.all(), empty_label="/", required=False)
	class Meta:
		model = Account
		fields = ('name', 'password', 'vhost', 'path')


class AccountUpdateForm(forms.ModelForm):
	new_password = forms.CharField(required=False, widget=forms.widgets.PasswordInput)
	class Meta:
		model = Account
		fields = ('vhost', 'path')

