from django import forms

from plum.core.models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'support_contact_email', 'support_contact_phone', 'support_contact_info',
                  'support_contact_url']
