import requests
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from plum.core.models import Vendor, Product, ProductScreenshot
from plum.front.forms import UploadedFileWidget


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'support_contact_email', 'support_contact_phone', 'support_contact_info',
                  'support_contact_url']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'long_description',
                  'stability', 'github_url',
                  'website_url', 'package_name']

    def clean_package_namae(self):
        pn = self.cleaned_data.get('package_name')
        if self.instance and self.instance.pk and self.instance.delivery_method != "pypi":
            return pn
        if pn:
            try:
                r = requests.get('https://pypi.org/pypi/{}/json'.format(pn))
                if r.status_code == 404:
                    raise ValidationError(_("This package was not found on PyPI. Please upload it there first!"))
                r.raise_for_status()
            except (requests.exceptions.BaseHTTPError, IOError) as e:
                raise ValidationError(_("We were unable to contact PyPI, please try again later."))

        return pn


class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = ProductScreenshot
        fields = ['picture', 'title']
        widgets = {
           'picture': UploadedFileWidget
        }


class UpdateProductForm(ProductForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'long_description',
                  'stability', 'github_url',
                  'website_url']
