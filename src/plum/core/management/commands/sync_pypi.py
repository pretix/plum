import logging
import requests
from datetime import datetime
from django.core.management import call_command
from django.core.management.base import BaseCommand

from plum.core.models import Product

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Automatically add new versions of PyPI packages"

    def handle(self, *args, **options):
        for p in Product.objects.filter(delivery_method=Product.DELIVERY_PYPI).exclude(package_name=""):
            try:
                r = requests.get('https://pypi.org/pypi/{}/json'.format(p.package_name))
                r.raise_for_status()
                d = r.json()
            except:
                logger.exception('Could not fetch metadata of "{}" from PyPI'.format(p))
            else:
                known = {v.name for v in p.versions.all()}
                for k, v in d['releases'].items():
                    if k in known:
                        continue
                    rel = [a for a in v if a['packagetype'] == 'bdist_wheel']
                    if not rel:
                        rel = v[0]
                    else:
                        rel = rel[0]
                    p.versions.create(
                        name=k,
                        release_date=datetime.strptime(rel['upload_time'][:10], '%Y-%m-%d').date(),
                        deliverable_url=rel['url'],
                    )
