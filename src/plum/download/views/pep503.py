import base64
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic import TemplateView, DetailView
from django_context_decorator import context

from plum.core.models import Product, Server
from plum.download.licenses import packages_with_active_license


class ServerAuthView:

    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token_type, _, credentials = auth_header.partition(' ')

        if token_type != 'Basic':
            return HttpResponse('Unauthorized', status=401)

        username, password = base64.b64decode(credentials).decode().split(':')
        try:
            server = Server.objects.get(pk=username)
        except Server.DoesNotExist:
            return HttpResponse('Unauthorized', status=401)

        if server.auth_token != password:
            return HttpResponse('Unauthorized', status=401)

        self.server = server

        return super().dispatch(request, *args, **kwargs)


class IndexView(ServerAuthView, TemplateView):
    template_name = 'download/pep503/index.html'

    @context
    def products(self):
        return packages_with_active_license([self.server])


class PackageView(ServerAuthView, DetailView):
    context_object_name = 'product'
    slug_url_kwarg = 'package'
    slug_field = 'package_name'
    template_name = 'download/pep503/package.html'

    def get_queryset(self):
        return packages_with_active_license([self.server])


class DownloadView(PackageView):

    def get(self, request, *args, **kwargs):
        version = get_object_or_404(self.get_object().versions.all(), pk=kwargs.get('version'))
        if not version.deliverable_file:
            return HttpResponse('No file available for this version', status=404)
        return FileResponse(version.deliverable_file)
