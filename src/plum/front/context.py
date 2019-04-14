from django.conf import settings

from plum.core.models import SiteConfiguration


def context_processor(request):
    return {
        'siteconf': SiteConfiguration.objects.get(),
    }
