import base64
import os
import re

from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView

from plum.core.models import Server, ProductVersion
from plum.download.licenses import packages_with_active_license


class PackageView(DetailView):
    context_object_name = 'product'
    slug_url_kwarg = 'package'
    slug_field = 'package_name'

    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if auth_header:
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

            self.servers = [server]
        elif request.user.is_authenticated:
            self.servers = Server.objects.filter(account__users__in=[self.request.user])
        else:
            self.servers = []

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return packages_with_active_license(self.servers)


class DownloadView(PackageView):

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            version = self.object.versions.get(pk=kwargs.get('version'))
        except Http404:
            return HttpResponse('This version either does not exist or you have no active license to download it.',
                                status=404)
        except (ValueError, ProductVersion.DoesNotExist, Http404):
            try:
                version = self.object.versions.get(name=kwargs.get('version'))
            except (ProductVersion.DoesNotExist, Http404):
                return HttpResponse('This version either does not exist or you have no active license to download it.',
                                    status=404)
        if not version.deliverable_file:
            return HttpResponse('No file available for this version', status=404)
        extension = os.path.splitext(version.deliverable_file.name)[1]
        vname = re.sub('[^a-zA-Z0-9.-]', '', version.name)
        return FileResponse(
            version.deliverable_file,
            as_attachment=True,
            filename=f'{self.object.package_name}-{vname}{extension}'
        )


class DownloadLatestView(PackageView):

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except (ProductVersion.DoesNotExist, Http404):
            return HttpResponse('This package either does not exist or you have no active license to download it.',
                                status=404)
        version = self.object.versions.first()
        if not version:
            return HttpResponse('No version available for this package', status=404)
        return redirect(reverse('download:file.download', kwargs={'package': self.object.package_name, 'version': version.pk}))
