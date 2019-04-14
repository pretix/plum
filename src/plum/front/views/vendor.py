from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from plum.core.models import Vendor
from plum.front.forms.vendor import VendorForm


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


class Edit(LoginRequiredMixin, UpdateView):
    model = Vendor
    template_name = 'front/vendor/edit.html'
    context_object_name = 'vendor'
    form_class = VendorForm

    def get_queryset(self):
        return Vendor.objects.filter(users__in=[self.request.user])
