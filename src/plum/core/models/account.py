# users/models.py
import os
import pytz
import uuid
from django.conf import settings

from django.db import models
from django.db.models import Exists, OuterRef
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    name = models.CharField(max_length=190, verbose_name=_('Name'))
    users = models.ManyToManyField('User')
    external_crm_id = models.CharField(max_length=190, blank=True)

    def __str__(self):
        return self.name


def gen_auth_token():
    return get_random_string(length=64)


class Server(models.Model):
    account = models.ForeignKey(Account, related_name='server', on_delete=models.PROTECT)
    url = models.URLField()
    is_evaluation = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=190, default=gen_auth_token)

    def __str__(self):
        return self.url

    def packages_with_active_license(self):
        from .product import Product
        from .license import License

        tz = pytz.timezone(settings.TIME_ZONE)
        today = now().astimezone(tz).date()

        return Product.objects.annotate(
            has_license=Exists(
                License.objects.filter(
                    servers__in=[self],
                    start_date__lte=today,
                    end_date__gte=today,
                    product_id=OuterRef('pk')
                )
            )
        ).filter(
            has_license=True
        )
