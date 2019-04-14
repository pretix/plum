from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from plum.core.models import SiteConfiguration


class Login(LoginView):
    template_name = 'front/auth/login.html'


class Logout(LogoutView):
    pass


class PasswordReset(PasswordResetView):
    template_name = "front/auth/reset.html"
    email_template_name = "front/auth/reset_email.html"
    subject_template_name = "front/auth/reset_email_subject.html"
    success_url = reverse_lazy('front:auth.login')

    def form_valid(self, form):
        messages.success(self.request, _('Great, we\'ll send you an email.'))
        return super().form_valid(form)

    @property
    def extra_email_context(self):
        return {
            'siteconf': SiteConfiguration.objects.get()
        }


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "front/auth/reset_confirm.html"
    success_url = reverse_lazy('front:auth.login')

    def form_valid(self, form):
        messages.success(self.request, _('We\'ve set your new password, you are good to go!'))
        return super().form_valid(form)
