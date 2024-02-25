from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from services.Uploader import Upload_to
from django.conf import settings
from services.Date import Date
from services.status import STATUS


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    about = models.TextField(_('about'), max_length=500, blank=True)
    profile_photo = models.ImageField(upload_to=Upload_to.user_profile_photo,  default='../static/assets/images/default.png', blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    token_key = models.CharField(max_length=50, null=True, unique=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='Available')

    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'settings.EMAIL_HOST_USER',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        return super(UserBase, self).save(*args, **kwargs)