from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Exists, OuterRef, Q
from django.utils.timezone import now

from ..core.models.license import License
from ..core.models.product import Product


def packages_with_active_license(servers):
    if not servers:
        return Product.objects.filter(is_paid=False)
    tz = ZoneInfo(settings.TIME_ZONE)
    today = now().astimezone(tz).date()

    return Product.objects.annotate(
        has_license=Exists(
            License.objects.filter(
                servers__in=servers,
                start_date__lte=today,
                end_date__gte=today,
                product_id=OuterRef('pk')
            )
        )
    ).filter(
        Q(has_license=True) | Q(is_paid=False)
    )
