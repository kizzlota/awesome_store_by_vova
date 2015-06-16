from django.db import models
from django.contrib import admin

import uuid
import os
# Create your models here.



def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('shoes_images', filename)


class Category(models.Model):
	name = models.CharField(max_length=200)

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
	                               default="/static/img/shoesimage.jpg")  # comix
	price = models.IntegerField()
	description = models.CharField(max_length=150, blank=True, null=True)
	category_name = models.ManyToManyField(Category)
	date = models.DateTimeField(null=True, auto_now_add=True)
	new_price = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	def image_tag(self):
		return u'<img src= "%s" width="64px" / >' % self.main_image.url

	image_tag.short_description = 'Image'
	image_tag.allow_tags = True

class PropertyImageInline(admin.TabularInline):
	model = Shoes.image.through
	extra = 3
	readonly_fields = ['row_name']
	def row_name(self, instance):
		return u'<img src="/media/%s" width="64px" / >' % instance.shoesphotos.images
	row_name.short_description = 'row_name2'
	row_name.allow_tags = True




class ShoesAdmin(admin.ModelAdmin):
	list_display = ["id", "name", "price", "date", "image_tag"]
	search_fields = ["name", "price"]
	# filter_horizontal = ('image',)
	exclude = ('image',)
	inlines = [PropertyImageInline, ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(ShoesPhotos, ShoesPhotosAdmin)
