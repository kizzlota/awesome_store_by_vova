from django.db import models
from django.contrib import admin
from mptt.models import MPTTModel, TreeForeignKey
from mptt.admin import MPTTModelAdmin
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('shoes_images', filename)


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class ShoesPhotos(models.Model):
    images = models.ImageField(blank=True, null=True, upload_to=get_file_path, default="/static/img/shoesimage.jpg")

    def __unicode__(self):
        return str(self.id)

    def image_tag(self):
        return u'<img src= "%s" width="120px" / >' % self.images.url

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class ShoeSizeParams(models.Model):
    size = models.CharField(max_length=50)
    height_shoe = models.CharField(max_length=50, null=True, blank=True)
    height_heel = models.CharField(max_length=50, null=True, blank=True)
    len_of_stelka = models.CharField(max_length=50, null=True, blank=True)
    len_of_feet = models.CharField(max_length=50, null=True, blank=True)
    shoe_bool = models.BooleanField(default=False)
    quantity = models.IntegerField()

    def __unicode__(self):
        return self.size


class ShoeParameters(models.Model):
    model_of_shoe = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50)
    date_manufac = models.DateField()
    price = models.IntegerField()
    new_price = models.IntegerField(blank=True, null=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    vkladka = models.CharField(max_length=50, null=True, blank=True)
    main_image = models.ImageField(blank=True, null=True, upload_to=get_file_path, default="/static/img/shoesimage.jpg")
    relation_to_shoes_photos = models.ManyToManyField(ShoesPhotos)
    rel_to_size = models.ManyToManyField(ShoeSizeParams)

    def min_value_filter(self):
        return min(self.price)

    def relation_to_photo(self):
        return self.relation_to_shoes_photos.all()

    relation_to_photo.short_description = 'relation'

    def relation_size(self):
        return self.rel_to_size.all()

    rel_to_size.short_description = 'relation_size'

    def __unicode__(self):
        return self.model_of_shoe + self.color


class Shoes(models.Model):
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=150, blank=True, null=True)
    category_name = models.ManyToManyField(Category)
    # date = models.DateTimeField(null=True, auto_now_add=True)
    relation_to_shoes_params = models.ManyToManyField(ShoeParameters)

    def __unicode__(self):
        return self.name

    def cat_name_for_shoe(self):
        return self.category_name.all()

    cat_name_for_shoe.short_description = 'category'
    cat_name_for_shoe.allow_tag = True
