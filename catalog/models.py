from django.db import models
from django.contrib import admin
from mptt.models import MPTTModel, TreeForeignKey
from mptt.admin import MPTTModelAdmin
import uuid
import os
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        user = self.model(username=username, email=self.normalize_email(email),
                          last_login=now, date_joined=now, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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

def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('shoes_images', filename)


class Category(MPTTModel):
	name = models.CharField(max_length=200, unique=True)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

	class MPTTMeta:
		order_insertion_by = ['name']

	def __unicode__(self):
		return self.name


class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name"]
	search_fields = ["name"]


class ShoesPhotos(models.Model):
	images = models.ImageField(blank=True, null=True, upload_to=get_file_path, default="/static/img/shoesimage.jpg")
	# des = models.IntegerField(null=True)

	def __unicode__(self):
		return self.images.name

	def image_tag(self):
		return u'<img src= "%s" width="120px" / >' % self.images.url

	image_tag.short_description = 'Image'
	image_tag.allow_tags = True


class ShoesPhotosAdmin(admin.ModelAdmin):
	list_display = ['images', 'image_tag']
	search_fields = ['images']
# readonly_fields = ('image_tag',)


class Shoes(models.Model):
	name = models.CharField(max_length=200)
	image = models.ManyToManyField(ShoesPhotos, blank=True)
	main_image = models.ImageField(blank=True, null=True, upload_to=get_file_path,
	                               default="/static/img/shoesimage.jpg")
	price = models.IntegerField()
	description = models.CharField(max_length=150, blank=True, null=True)
	category_name = models.ManyToManyField(Category)
	date = models.DateTimeField(null=True, auto_now_add=True)
	quantity = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

	def image_tag(self):
		return u'<img src= "%s" width="64px" / >' % self.main_image.url

	image_tag.short_description = 'Image'
	image_tag.allow_tags = True

	def cat_name_for_shoe(self):
		return self.category_name.all()

	cat_name_for_shoe.short_description = 'category'
	cat_name_for_shoe.allow_tag = True

class PropertyImageInline(admin.TabularInline):
	model = Shoes.image.through
	extra = 3
	readonly_fields = ['row_name']
	def row_name(self, instance):
		return u'<img src="/media/%s" width="64px" / >' % instance.shoesphotos.images
	row_name.short_description = 'row_name2'
	row_name.allow_tags = True


class ShoesAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "price", "date", "image_tag", "cat_name_for_shoe", "quantity"]
	search_fields = ["name", "price", "quantity"]
	# filter_horizontal = ('image',)
	exclude = ('image',)
	inlines = [PropertyImageInline, ]


class RegistrationCode(models.Model):
	code = models.CharField(max_length=255)
	username = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)

class RegistrationCodeAdmin(admin.ModelAdmin):
	list_display = ['code', 'username', 'date']

admin.site.register(RegistrationCode, RegistrationCodeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(ShoesPhotos, ShoesPhotosAdmin)
