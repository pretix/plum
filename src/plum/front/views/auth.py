from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from plum.core.models import SiteConfiguration, User
from plum.front.forms.auth import RegistrationForm


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
            'siteconf': SiteConfiguration.get_solo()
        }


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "front/auth/reset_confirm.html"
    success_url = reverse_lazy('front:auth.login')

    def form_valid(self, form):
        messages.success(self.request, _('We\'ve set your new password, you are good to go!'))
        return super().form_valid(form)


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = "front/auth/password_change.html"
    success_url = reverse_lazy('front:index')

    def form_valid(self, form):
        messages.success(self.request, _('We\'ve set your new password, you are good to go!'))
        return super().form_valid(form)


class UserIndex(LoginRequiredMixin, TemplateView):
    template_name = "front/user_index.html"


def register(request):
    ctx = {}
    if request.user.is_authenticated:
        return redirect(request.GET.get("next", 'control:index'))
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['email'],
                form.cleaned_data['password'],
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('front:user.index')
    else:
        form = RegistrationForm()
    ctx['form'] = form
    return render(request, 'front/auth/register.html', ctx)
