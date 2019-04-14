from django import forms
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.utils.translation import ugettext_lazy as _

from plum.core.models import User


class RegistrationForm(forms.Form):
    error_messages = {
        'duplicate_email': _("You already registered with that email address, please use the login form."),
        'pw_mismatch': _("Please enter the same password twice"),
    }
    email = forms.EmailField(
        label=_('Email address'),
        required=True
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'  # see https://bugs.chromium.org/p/chromium/issues/detail?id=370363#c7
        }),
        required=True
    )
    password_repeat = forms.CharField(
        label=_('Repeat password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'  # see https://bugs.chromium.org/p/chromium/issues/detail?id=370363#c7
        }),
        required=True
    )

    def clean(self):
        password1 = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password_repeat')

        if password1 and password1 != password2:
            raise forms.ValidationError({
                'password_repeat': self.error_messages['pw_mismatch'],
            }, code='pw_mismatch')
        return self.cleaned_data

    def clean_password(self):
        password1 = self.cleaned_data.get('password', '')
        user = User(email=self.cleaned_data.get('email'))
        if validate_password(password1, user=user) is not None:
            raise forms.ValidationError(_(password_validators_help_texts()), code='pw_invalid')
        return password1

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                self.error_messages['duplicate_email'],
                code='duplicate_email'
            )
        return email
