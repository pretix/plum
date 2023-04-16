# users/models.py
import hashlib
import os
import re
import uuid

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from functools import partial


def icon_filename(instance, filename):
    return 'icon/{}/{}{}'.format(instance.pk, str(uuid.uuid4()), os.path.splitext(filename)[1])


class Vendor(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Name'))
    certified = models.BooleanField(default=False, verbose_name=_('Certified vendor'))
    support_contact_phone = models.CharField(max_length=190, verbose_name=_('Support phone number'), blank=True)
    support_contact_email = models.EmailField(blank=True, verbose_name=_('Support email address'))
    support_contact_url = models.URLField(blank=True, verbose_name=_('Support form URL'))
    support_contact_info = models.TextField(blank=True, verbose_name=_('Additional support information'))
    users = models.ManyToManyField('User', related_name='vendors')

    def __str__(self):
        return self.name


def gen_upload_key(*args):
    return get_random_string(length=64)


class Product(models.Model):
    DELIVERY_PYPI = 'pypi'
    DELIVERY_LOCALPIP = 'pip'
    DELIVERY_BUNDLED = 'bundled'
    DELIVERY_ANDROID = 'android'
    DELIVERY_FILE = 'file'
    DELIVERY_EXTERNAL = 'external'
    DELIVERY_METHODS = (
        (DELIVERY_PYPI, _('PyPI')),
        (DELIVERY_LOCALPIP, _('Local python package index')),
        (DELIVERY_BUNDLED, _('Bundled')),
        (DELIVERY_ANDROID, _('Android app')),
        (DELIVERY_FILE, _('File')),
        (DELIVERY_EXTERNAL, _('External store')),
    )

    TIMEFRAME_MONTHLY = 'monthly'
    TIMEFRAME_YEARLY = 'yearly'
    TIMEFRAME_LIFETIME = 'lifetime'

    PRICING_TIMEFRAMES = (
        (TIMEFRAME_MONTHLY, _('monthly')),
        (TIMEFRAME_YEARLY, _('yearly')),
        (TIMEFRAME_LIFETIME, _('one-off'))
    )

    STABILITY_ALPHA = 'alpha'
    STABILITY_BETA = 'beta'
    STABILITY_STABLE = 'stable'
    STABILITY_DISCONTINUED = 'discontinued'

    STABILITY_VALUES = (
        (STABILITY_ALPHA, _('alpha')),
        (STABILITY_BETA, _('beta')),
        (STABILITY_STABLE, _('stable')),
        (STABILITY_DISCONTINUED, _('discontinued')),
    )

    name = models.CharField(max_length=190, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    category = models.ForeignKey('Category', verbose_name=_('Product category'), on_delete=models.PROTECT,
                                 related_name='products')
    vendor = models.ForeignKey('Vendor', verbose_name=_('Product vendor'), on_delete=models.PROTECT, null=False,
                               related_name='products')
    long_description = models.TextField(verbose_name=_('Long description'))
    approved = models.BooleanField(default=False, verbose_name=_('Approved and visible'))
    certified = models.BooleanField(default=False, verbose_name=_('Certified plugin'))
    unlisted = models.BooleanField(default=False, verbose_name=_('Unlisted'))
    icon = models.FileField(null=True, upload_to=icon_filename, blank=True)

    stability = models.CharField(choices=STABILITY_VALUES, max_length=190, verbose_name=_('Stability'))
    delivery_method = models.CharField(choices=DELIVERY_METHODS, max_length=190, verbose_name=_('Delivery method'))

    is_paid = models.BooleanField(default=False)
    pricing_tiers_variable = models.ForeignKey('PriceVariable', verbose_name=_('Pricing variable'), null=True,
                                               on_delete=models.PROTECT, blank=True)
    pricing_timeframe = models.CharField(choices=PRICING_TIMEFRAMES, verbose_name=_('Pricing timeframe'),
                                         null=True, max_length=190, blank=True)

    github_url = models.URLField(blank=True, verbose_name=_('GitHub URL'))
    external_store_url = models.URLField(blank=True, verbose_name=_('External store URL'))
    website_url = models.URLField(blank=True, verbose_name=_('Website URL'))
    package_name = models.CharField(blank=False, null=True, unique=True, max_length=190, verbose_name=_('Package name'),
                                    help_text=_('Should be a valid Python package name. For free packages, this is the name the package should have on on PyPI.'))

    android_package_name = models.CharField(blank=True, null=True, unique=True, max_length=190)
    android_is_on_gplay = models.BooleanField(default=False)

    upload_key = models.CharField(max_length=64, default=gen_upload_key)

    class Meta:
        verbose_name = _('Product')
        ordering = ("-certified", "name",)

    def __str__(self):
        return self.name

    @property
    def visible_tiers(self):
        return self.tiers.filter(visible=True)

    def save(self, *args, **kwargs):
        if self.package_name:
            self.package_name = re.sub(r"[-_.]+", "-", self.package_name).lower()
        return super().save(*args, **kwargs)


def screenshot_filename(instance, filename):
    return 'screenshots/{}/{}{}'.format(instance.product_id, str(uuid.uuid4()), os.path.splitext(filename)[1])


class ProductScreenshot(models.Model):
    product = models.ForeignKey(Product, related_name='screenshots', on_delete=models.CASCADE)
    picture = models.ImageField(verbose_name=_('Picture'), upload_to=screenshot_filename, blank=False)
    title = models.CharField(max_length=190, verbose_name=_('title'), blank=False)

    class Meta:
        verbose_name = _('Screenshot')


def deliverable_filename(instance, filename):
    return 'deliverables/{}/{}{}'.format(instance.product_id, str(uuid.uuid4()), os.path.splitext(filename)[1])


class ProductVersion(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.CASCADE)
    name = models.CharField(max_length=190, verbose_name=_('Version name'))
    release_date = models.DateField()
    release_notes = models.TextField(blank=True)

    deliverable_url = models.URLField(blank=True)
    deliverable_file = models.FileField(null=True, upload_to=deliverable_filename, blank=True)
    deliverable_file_checksum = models.CharField(blank=True, max_length=255)
    deliverable_file_name = models.CharField(blank=True, max_length=255)
    deliverable_file_size = models.BigIntegerField(blank=True, null=True)

    min_platform_version = models.ForeignKey('PlatformVersion', on_delete=models.PROTECT, related_name='products_from',
                                             verbose_name=_('Minimum platform version'), null=True, blank=True)
    max_platform_version = models.ForeignKey('PlatformVersion', on_delete=models.PROTECT, related_name='products_upto',
                                             verbose_name=_('Maximum platform version'), null=True, blank=True)
    android_index_data = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ("-release_date", "-pk")

    def save(self, *args, **kwargs):
        if self.deliverable_file and not self.deliverable_file_checksum:
            hasher = hashlib.sha256()
            for buf in iter(partial(self.deliverable_file.read, 65536), b''):
                hasher.update(buf)
            self.deliverable_file_checksum = hasher.hexdigest()
        if self.deliverable_file and not self.deliverable_file_size:
            self.deliverable_file_size = self.deliverable_file.size
        return super().save(*args, **kwargs)


class ProductPriceTier(models.Model):
    product = models.ForeignKey(Product, related_name='tiers', on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    up_to_value = models.IntegerField(verbose_name=_('Maximum value of pricing variable'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))

    def __str__(self):
        return str(self.up_to_value)

    class Meta:
        ordering = ("up_to_value",)
