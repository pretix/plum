import base64
import re

from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django_context_decorator import context

from plum.core.models import Product, Server


class UploaderAuthView:

    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token_type, _, credentials = auth_header.partition(' ')

        if token_type != 'Basic':
            return HttpResponse('Unauthorized', status=401)

        username, password = base64.b64decode(credentials).decode().split(':')
        try:
            prod = Product.objects.get(slug=username)
        except Product.DoesNotExist:
            return HttpResponse('Unauthorized', status=401)

        if prod.upload_key != password:
            return HttpResponse('Unauthorized', status=401)

        self.product = prod

        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class UploadView(UploaderAuthView, View):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return HttpResponse('No file given', status=400)
        f = request.FILES['file']

        if self.product.delivery_method == Product.DELIVERY_LOCALPIP:
            # https://www.python.org/dev/peps/pep-0427/#file-name-convention
            fname = re.compile('^([a-z0-9_]+)-([0-9][a-z0-9.]*)(-[^-]+)?-([^-]+)-([^-]+)-([^-]+)\\.whl$')
            m = fname.match(f.name)
            if not m:
                return HttpResponse('Invalid wheel file name', status=400)
            if m.group(1) != re.sub(r"[^\w\d.]+", "_", self.product.package_name, re.UNICODE):
                return HttpResponse('Invalid package name in filename', status=400)
            if m.group(5) != 'none' or m.group(6) != 'any':
                return HttpResponse('Only wheels of type none-any are currently supported', status=400)
            version = m.group(2)
        elif self.product.delivery_method == Product.DELIVERY_FILE:
            if 'version' not in request.POST:
                return HttpResponse('Please supply a version name', status=400)
            version = request.POST.get('version')
        else:
            return HttpResponse('Package does not allow uploads', status=400)


        if self.product.versions.filter(name=version).exists():
            return HttpResponse('Version already exists', status=400)
        v = self.product.versions.create(
            name=version,
            release_date=now().date(),
            deliverable_file_name=f.name
        )
        v.deliverable_file.save(f.name, f)
        return HttpResponse('OK!', status=201)
