from django.db import models
from django.contrib import admin

# Create your models here.

class TestShoesPhotos(models.Model):
	image = models.CharField(max_length=100)

	def __unicode__(self):
		return self.image


class TestShoesParams(models.Model):
	color = models.CharField(max_length=100)
	# size
	# queantity
	# main_photo
	relation_to_photos = models.ManyToManyField(TestShoesPhotos)

	def relation_photos(self):
		return self.relation_to_photos.all()
	relation_photos.short_description = 'relation'

	def __unicode__(self):
		return self.color


class TestShoes(models.Model):
	name = models.CharField(max_length=200)
	relation_to_test = models.ManyToManyField(TestShoesParams)

	def __unicode__(self):
		return self.name


class TestShoesAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']


class TestShoesParamasAdmin(admin.ModelAdmin):
	list_display = ['id', 'color', 'relation_photos']

class TestShoesPhotosAdmin(admin.ModelAdmin):
	list_display = ['id', 'image']


admin.site.register(TestShoes, TestShoesAdmin)
admin.site.register(TestShoesParams, TestShoesParamasAdmin)
admin.site.register(TestShoesPhotos, TestShoesPhotosAdmin)