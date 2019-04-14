from django.db import models
from pycountry import currencies
from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    CURRENCY_CHOICES = [(c.alpha_3, c.alpha_3 + " - " + c.name) for c in currencies]

    site_name = models.CharField(max_length=255, default="pretix Marketplace")
    vendor_contact = models.EmailField(default='marketplace@pretix.eu')
    buyer_contact = models.EmailField(default='support@pretix.eu')
    front_page_intro = models.TextField(
        default="Welcome to the pretix Marketplace! If you're hosting pretix yourself, this is the place where "
                "you can find plugins to extend your installation. If you use pretix through our pretix Hosted offering, "
                "you do not need this page, most useful plugins are already installed for you."
    )
    footer_column_1 = models.TextField(
        default='<h5>About</h5><ul class="list-unstyled text-small">'
                '<li><a class="text-muted" href="https://pretix.eu">pretix.eu</a></li>'
                '</ul>'
    )
    footer_column_2 = models.TextField(
        default='<h5>Tech</h5><ul class="list-unstyled text-small">'
                '<li><a class="text-muted" href="https://docs.pretix.eu">Docs</a></li>'
                '</ul>'
    )
    footer_column_3 = models.TextField(
        default='<h5>Legal</h5><ul class="list-unstyled text-small">'
                '<li><a class="text-muted" href="https://pretix.eu/about/en/imprint">Imprint</a></li>'
                '<li><a class="text-muted" href="https://pretix.eu/about/en/privacy">Privacy</a></li>'
                '</ul>'
    )
    currency = models.CharField(max_length=10,
                                choices=CURRENCY_CHOICES,
                                default="EUR")
    pre_install_commands = models.TextField(
        default='$ source /var/pretix/venv/bin/activate'
    )
    post_install_commands = models.TextField(
        default='(venv)$ python -m pretix migrate\n'
                '(venv)$ python -m pretix rebuild\n'
                '# systemctl restart pretix-web pretix-worker'
    )
    doc_installation = models.URLField(
        default='https://docs.pretix.eu/en/latest/admin/installation/index.html'
    )

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
