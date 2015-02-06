from django import forms
from models import Account
from web.models import VHost

class AccountCreateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.widgets.PasswordInput)
	vhost    = forms.ModelChoiceField(queryset=VHost.objects.all(), empty_label="/")
	class Meta:
		model = Account


class AccountUpdateForm(forms.ModelForm):
	new_password = forms.CharField(required=False, widget=forms.widgets.PasswordInput)
	class Meta:
		model = Account
		fields = ('vhost', 'path')

