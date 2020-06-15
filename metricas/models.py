from django.db import models


class Metrica(models.Model):
    nome = models.CharField(max_length=200)
    data = models.DateTimeField('date published')
    valor = models.IntegerField()


from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import re
import datetime
from django.core.mail import send_mail
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=True, is_active=True, last_login2=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, True, **extra_fields)
    
    



class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(_('username'), max_length=15, unique=True, help_text=_('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'), validators=[ validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))])
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), default=timezone.now, blank=True, null=True)
    last_login2 = models.DateTimeField(_('last login2'), default=timezone.now)
    previous_password = models.CharField(_('previous password'), max_length=128, default='')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    def get_full_name(self):
        full_name = '%s %s' % (self.username, self.email)
        return full_name.strip()
    def get_short_name(self):
        return self.username
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        print(timezone.now())
        print(self.date_joined)
        if self.date_joined == self.last_login2:
            print("date joined == last login")
            if timezone.now() - self.date_joined > datetime.timedelta(minutes=1):
                User.objects.get(username=self.username).delete()
                print("date joined > 1min | Usuario deletado")
                #return False

        if timezone.now() - self.last_login2 > datetime.timedelta(minutes=2):
            print("last login > 2 min | is_active = False")
            #self.is_active = False
        
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)
