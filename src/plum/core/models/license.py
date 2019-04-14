# users/models.py
import os
import pytz
import uuid
from django.conf import settings

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class License(models.Model):
    account = models.ForeignKey('Account', related_name='licenses', on_delete=models.PROTECT)
    servers = models.ManyToManyField('Server', related_name='licenses')
    product = models.ForeignKey('Product', related_name='licenses', on_delete=models.PROTECT)
    pricing_tier = models.ForeignKey('ProductPriceTier', related_name='licenses', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ('-end_date', '-start_date')

    @property
    def is_expired(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        today = now().astimezone(tz).date()
        return self.end_date < today
