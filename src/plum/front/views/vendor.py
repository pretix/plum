from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView
from django_context_decorator import context
from urllib.parse import urljoin

from plum.core.models import Vendor, Product, SiteConfiguration, ProductScreenshot
from plum.front.forms.vendor import VendorForm, ProductForm, UpdateProductForm, ScreenshotForm


class Create(LoginRequiredMixin, CreateView):
    template_name = 'front/vendor/create.html'
    model = Vendor
    form_class = VendorForm

    def form_valid(self, form):
        s = super().form_valid(form)
        form.instance.users.add(self.request.user)
        return s

    def get_success_url(self):
        return reverse("front:vendor.index", kwargs={'pk': self.object.pk})


class Detail(LoginRequiredMixin, DetailView):
    model = Vendor
    template_name = 'front/vendor/index.html'
    context_object_name = 'vendor'

    def get_queryset(self):
        return Vendor.objects.filter(
            users__in=[self.request.user]
        )


class CreatePaidProduct(Detail):
    template_name = 'front/vendor/product_create_paid.html'


class Edit(LoginRequiredMixin, UpdateView):
    model = Vendor
    template_name = 'front/vendor/edit.html'
    context_object_name = 'vendor'
    form_class = VendorForm

    def get_queryset(self):
        return Vendor.objects.filter(users__in=[self.request.user])


class CreateProduct(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'front/vendor/product_create.html'

    @cached_property
    def vendor(self):
        return get_object_or_404(
            Vendor.objects.filter(users__in=[self.request.user]),
            pk=self.kwargs.get('vendor')
        )

    @transaction.atomic
    def form_valid(self, form):
        messages.success(self.request, _('Your product has been created. We will automatically add your releases from PyPI in the next hours. '
                                         'As soon as the plugin has been reviewed by our staff, it will be published.'))
        form.instance.vendor = self.vendor
        form.instance.is_paid = False
        form.instance.delivery_method = "pypi"
        s = super().form_valid(form)

        sc = SiteConfiguration.get_solo()
        subject = "New product on {}".format(sc.site_name)
        body = 'Please review {}'.format(
            urljoin(settings.SITE_URL, reverse('admin:core_product_change', args=(form.instance.pk,)))
        )
        email_message = EmailMultiAlternatives(subject, body, settings.SERVER_EMAIL, [sc.vendor_contact])
        email_message.send()
        return s

    def get_success_url(self):
        return reverse("front:vendor.index", kwargs={'pk': self.vendor.pk})

    @context
    @cached_property
    def formset(self):
        formsetclass = inlineformset_factory(
            Product, ProductScreenshot,
            form=ScreenshotForm,
            can_order=False, can_delete=True, extra=0
        )
        return formsetclass(self.request.POST if self.request.method == "POST" else None,
                            self.request.FILES if self.request.method == "POST" else None)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid() and self.formset.is_valid():
            with transaction.atomic():
                r = self.form_valid(form)
                for f in self.formset:
                    f.instance.product = self.object
                    f.save()
                return r
        return self.form_invalid(form)


class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = UpdateProductForm
    context_object_name = 'product'
    template_name = 'front/vendor/product_edit.html'

    @cached_property
    def vendor(self):
        return get_object_or_404(
            Vendor.objects.filter(users__in=[self.request.user]),
            pk=self.kwargs.get('vendor')
        )

    def form_valid(self, form):
        messages.success(self.request, _('Your changes have been saved.'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("front:vendor.index", kwargs={'pk': self.vendor.pk})

    @context
    @cached_property
    def formset(self):
        formsetclass = inlineformset_factory(
            Product, ProductScreenshot,
            form=ScreenshotForm,
            can_order=False, can_delete=True, extra=0
        )
        return formsetclass(self.request.POST if self.request.method == "POST" else None,
                            self.request.FILES if self.request.method == "POST" else None,
                            instance=self.object)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid() and self.formset.is_valid():
            with transaction.atomic():
                for f in self.formset:
                    if f in self.formset.deleted_forms:
                        continue
                    f.instance.product = self.object
                    f.save()
                return self.form_valid(form)
        return self.form_invalid(form)
