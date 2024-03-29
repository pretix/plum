# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField(_('email address'), blank=True, unique=True)

    @staticmethod
    def create_user(email, password=None, **extra_fields):
        def _create_user(email, password, **extra_fields):
            if not email:
                raise ValueError('The given email must be set')
            email = User.objects.normalize_email(email)
            user = User(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return _create_user(email, password, **extra_fields)
