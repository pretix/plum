from django import forms

from plum.core.models import Account, Server


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'primary_email', 'primary_name', 'address_supplement',
                  'address_street', 'address_zipcode', 'address_city', 'address_country',
                  'address_vat_id']


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['url']
