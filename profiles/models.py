from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        user = self.model(username=username, email=self.normalize_email(email),
                          last_login=now, date_joined=now, **extra_fields)
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAddress(models.Model):
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=1500, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return self.phone


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True,
                                help_text=_(
                                    'Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'))
    email = models.EmailField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_staff = models.BooleanField(default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=False,
                                    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Additions fields
    social_img_url = models.CharField(max_length=120, blank=True, null=True)
    profile_image = models.ImageField(upload_to="uploads", blank=False, null=False,
                                      default="/static/img/users/defaultuserimage.png")

    user_bio = models.TextField(max_length=1200, blank=True)

    user_details = models.ForeignKey(UserAddress, null=True, default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    # def email_user(self, subject, message, from_email=None):
    #    send_mail(subject, message, from_email, [self.email])
    def __unicode__(self):
        return self.username



class RegistrationCode(models.Model):
    code = models.CharField(max_length=255)
    username = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

