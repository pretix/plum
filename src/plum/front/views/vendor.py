from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView

from plum.core.models import Vendor, Product
from plum.front.forms.vendor import VendorForm, ProductForm, UpdateProductForm


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

    def form_valid(self, form):
        messages.success(self.request, _('Your product has been created. We will automatically add your releases from PyPI in the next hours. '
                                         'As soon as the plugin has been reviewed by our staff, it will be published.'))
        form.instance.vendor = self.vendor
        form.instance.is_paid = False
        form.instance.delivery_method = "pypi"
        s = super().form_valid(form)
        return s

    def get_success_url(self):
        return reverse("front:vendor.index", kwargs={'pk': self.vendor.pk})


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
