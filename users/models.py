from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from app.models import Photo


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        elif not email:
            raise ValueError('The given email must be set')

        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)

# 参考：https://qiita.com/okoppe8/items/10ae61808dc3056f9c8e


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=50, unique=True, error_messages={
                                'unique': _("That username already exists."), },)
    email = models.EmailField(_('email address'), unique=True)
    # 中間テーブル
    fav_photos = models.ManyToManyField(Photo, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    # ↓superuser作るときに必要なものを定義。USERNAME_FIELDに指定したものとpasswordはdefaultで要求される。
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # email_user関数は、AbstractUserの中で定義されている関数のため、AbstractBaseUserでモデルを作っているときは、関数を定義してやる必要がある。https://github.com/django/django/blob/master/django/contrib/auth/models.py
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
