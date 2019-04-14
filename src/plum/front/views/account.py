from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import CreateView, DetailView, UpdateView
from django_context_decorator import context

from plum.core.models import Account, Server
from plum.front.forms.account import AccountForm, ServerForm


class Create(LoginRequiredMixin, CreateView):
    template_name = 'front/account/create.html'
    model = Account
    form_class = AccountForm

    def form_valid(self, form):
        s = super().form_valid(form)
        form.instance.users.add(self.request.user)
        return s

    def get_success_url(self):
        return reverse("front:account.index", kwargs={'pk': self.object.pk})


class Detail(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'front/account/index.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Account.objects.filter(
            users__in=[self.request.user]
        ).prefetch_related(
            'servers', 'servers__licenses', 'servers__licenses__product', 'servers__licenses__pricing_tier',
            'licenses__product__pricing_tiers_variable'
        )

    @context
    def schema(self):
        return settings.SITE_URL.split('://')[0]

    @context
    def domain(self):
        return settings.SITE_URL.split('://')[1]


class Edit(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'front/account/edit.html'
    context_object_name = 'account'
    form_class = AccountForm

    def get_queryset(self):
        return Account.objects.filter(users__in=[self.request.user])


class CreateServer(LoginRequiredMixin, CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'front/account/server_create.html'

    @cached_property
    def account(self):
        return get_object_or_404(
            Account.objects.filter(users__in=[self.request.user]),
            pk=self.kwargs.get('account')
        )

    def form_valid(self, form):
        form.instance.account = self.account
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("front:account.index", kwargs={'pk': self.account.pk})
