# users/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class PlatformVersion(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Version name'))
    release_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class PriceVariable(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Variable name'))

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Category name'))

    class Meta:
        verbose_name = _('Category')
        ordering = ('name',)

    def __str__(self):
        return self.name
