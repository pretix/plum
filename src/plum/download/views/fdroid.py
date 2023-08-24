import datetime
import json
import os
import subprocess
import tempfile
import time
from collections import UserDict
from urllib.parse import urljoin

from django.conf import settings
from django.db.models import Prefetch, Max
from django.http import FileResponse, Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from fdroidserver import signindex, common

from plum.core.models import SiteConfiguration, Product, ProductVersion, ProductScreenshot
from plum.download.licenses import packages_with_active_license
from plum.settings import DATA_DIR


def create_keystore_if_not_exists(name):
    if os.path.exists(name):
        return
    subprocess.check_call([
        'keytool',
        '-genkey', '-v',
        '-keystore', name,
        '-alias', 'plum',
        '-keyalg', 'RSA',
        '-keysize', '2048',
        '-validity', '10000',
        '-storepass', 'wellknown',
        '-keypass', 'wellknown',
        '-dname', 'CN=, OU=, O=, L=, S=, C='
    ])


class IndexView(ListView):
    context_object_name = 'product'
    slug_url_kwarg = 'package'
    slug_field = 'package_name'

    def get_queryset(self):
        return packages_with_active_license([]).filter(
            delivery_method=Product.DELIVERY_ANDROID,
            android_package_name__isnull=False,
            approved=True,
        ).select_related('vendor', 'category').prefetch_related(
            Prefetch(
                'versions',
                queryset=ProductVersion.objects.filter(android_index_data__isnull=False),
                to_attr='active_versions'
            ),
            'screenshots',
        )

    def get(self, request, *args, **kwargs):
        siteconf = SiteConfiguration.get_solo()
        data = {
            "repo": {
                "timestamp": int(time.time() * 1000),
                "version": int(ProductVersion.objects.aggregate(m=Max('pk'))['m'] or None),
                "maxage": 14,
                "name": siteconf.site_name,
                "icon": "fdroid-icon.png",  # TODO, but seems to be unused?
                "address": f"{settings.SITE_URL}/",
                "description": f"Packages from {siteconf.site_name}",
            },
            "requests": {
                "install": [],
                "uninstall": []
            },
            "apps": [],
            "packages": {}
        }
        for p in self.get_queryset():
            if p.active_versions:
                app, package = self._app_for_product(p)
                data['apps'].append(app)
                data['packages'][p.android_package_name] = package

        with tempfile.TemporaryDirectory() as tmpdir:
            with open(f'{tmpdir}/index-v1.json', 'w') as json_file:
                json.dump(data, json_file, indent=2)

            common.config = signindex.config = {
                'jarsigner': 'jarsigner',
                'repo_keyalias': 'plum',
                'keystore': os.path.join(DATA_DIR, 'fdroid.keystore'),
                'keystorepass': 'wellknown',
                'keypass': 'wellknown',
            }
            common.options = UserDict()
            common.options.verbose = False
            create_keystore_if_not_exists(os.path.join(DATA_DIR, 'fdroid.keystore'))
            signindex.sign_index(tmpdir, 'index-v1.json')

            return FileResponse(open(os.path.join(tmpdir, 'index-v1.jar'), 'rb'))

    def _app_for_product(self, product):
        app = {
            "categories": [
                product.category.name
            ],
            "changelog": urljoin(settings.SITE_URL,
                                 reverse("front:product.versions", kwargs={'product': product.slug})),
            "suggestedVersionName": product.active_versions[0].android_index_data['versionName'],
            "suggestedVersionCode": str(product.active_versions[0].android_index_data['versionCode']),
            "license": "",
            "webSite": product.website_url,
            "added": int(datetime.datetime.combine(
                min(v.release_date for v in product.active_versions), datetime.time(0, 0, 0)
            ).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000),
            "icon": f'{product.package_name}.png' if product.icon else None,
            "packageName": product.android_package_name,
            "lastUpdated": int(datetime.datetime.combine(
                max(v.release_date for v in product.active_versions), datetime.time(0, 0, 0)
            ).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000),
            "localized": {
                "en-US": {
                    "description": product.long_description,
                    "name": product.name,
                    "phoneScreenshots": [
                        f'{s.pk}.png' for s in product.screenshots.all()
                    ],
                    "summary": product.long_description.split(".")[0].split("\n")[0],
                },
            }
        }
        package = []
        for v in product.active_versions:
            package.append({
                **v.android_index_data,
                "added": int(datetime.datetime.combine(
                    v.release_date, datetime.time(0, 0, 0)
                ).replace(tzinfo=datetime.timezone.utc).timestamp() * 1000),
                "apkName": f'{product.package_name}_{v.pk}.apk',
            })
        return app, package


class IconView(DetailView):
    slug_url_kwarg = 'package'
    slug_field = 'package_name'
    queryset = Product.objects.filter(approved=True)

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.icon:
            raise Http404()
        return FileResponse(object.icon.open())


class ScreenshotView(DetailView):
    pk_url_kwarg = 'id'
    queryset = ProductScreenshot.objects.filter(product__approved=True)

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.picture:
            raise Http404()
        return FileResponse(object.picture.open())
