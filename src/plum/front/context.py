from plum.core.models import SiteConfiguration


def context_processor(request):
    return {
        'siteconf': SiteConfiguration.objects.get()
    }
