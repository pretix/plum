from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Account(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Company name'))
    users = models.ManyToManyField('User', related_name='accounts')

    primary_email = models.EmailField(verbose_name=_('Primary contact email'),
                                      help_text=_('We will contact you at this address for everything concerning '
                                                  'your contract, billing, invoices, and important informations '
                                                  'about your purchases.'),
                                      default='')
    primary_phone = models.CharField(verbose_name=_('Contact phone number'), max_length=190,
                                     default='')
    primary_name = models.CharField(verbose_name=_('Primary contact person'), max_length=190,
                                    default='')
    address_supplement = models.CharField(verbose_name=_('Address supplement'), default='', max_length=190,
                                          blank=True)
    address_street = models.CharField(verbose_name=_('Address'), default='', max_length=190)
    address_zipcode = models.CharField(verbose_name=_('ZIP code'), default='', max_length=190)
    address_city = models.CharField(verbose_name=_('City'), default='', max_length=190)
    address_country = CountryField(verbose_name=_('Country'), default='DE')
    address_vat_id = models.CharField(verbose_name=_('EU VAT ID'), default='', max_length=190,
                                      help_text=_('If you are located in the EU but outside Germany, we need your '
                                                  'VAT ID. If you do not provide one, we will need to charge you '
                                                  'VAT on our services and can not issue reverse charge invoices.'),
                                      blank=True)

    external_crm_id = models.CharField(max_length=190, blank=True)

    def __str__(self):
        return self.name


def gen_auth_token():
    return get_random_string(length=64)


class Server(models.Model):
    account = models.ForeignKey(Account, related_name='servers', on_delete=models.PROTECT)
    url = models.URLField(verbose_name=_("URL"), help_text=_("The base URL the platform runs at"))
    is_evaluation = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=190, default=gen_auth_token)

    def __str__(self):
        return self.url
