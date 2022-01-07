import logging
import tempfile

from django.core.management.base import BaseCommand
from fdroidserver import scan_apk

from plum.core.models import Product, ProductVersion

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Scan newly added APK files"

    def handle(self, *args, **options):
        for pv in ProductVersion.objects.filter(product__delivery_method=Product.DELIVERY_ANDROID,
                                                android_index_data__isnull=True):
            with tempfile.NamedTemporaryFile() as f:
                f.write(pv.deliverable_file.open('rb').read())
                f.flush()
                d = scan_apk(f.name)
                d.pop('antiFeatures', None)
                pv.android_index_data = d
                pv.save(update_fields=['android_index_data'])
