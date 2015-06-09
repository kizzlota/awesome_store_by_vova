from django.db import models
from django.contrib import admin
# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

# gg fgf
class CategoryAdmin(admin.ModelAdmin):
	list_display = ["name"]
	search_fields = ["name"]


class Shoes(models.Model):
	name = models.CharField(max_length=200)
	image = models.ImageField(blank=True, null=True, upload_to='shoes_images', default="/static/img/shoesimage.jpg")
	price = models.IntegerField()
	description = models.CharField(max_length=150, blank=True, null=True)
	category_name = models.ForeignKey(Category)
	date = models.DateTimeField(null=True, auto_now_add=True)
	new_price = models.IntegerField(null=True, blank=True)

	def __unicode__(self):
		return self.name



class ShoesAdmin(admin.ModelAdmin):
	list_display = ["name", "price", "category_name", "date"]
	search_fields = ["name", "price", "category_name"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Shoes, ShoesAdmin)


