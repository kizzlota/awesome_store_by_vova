from django.db import models
from django.contrib import admin
from catalog.models import Shoes


# Create your models here.


class BasketModel(models.Model):
	data_user_hash = models.CharField(max_length=200)
	quantity = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	shoes_id = models.ForeignKey(Shoes)

	@property
	def info_mesht(self):
		return self.shoes_id


class BasketAdmin(admin.ModelAdmin):
	list_display = ["data_user_hash", "quantity", "date", "shoes_id"]
	search_fields = ["data_user_hash", "date"]


class OrderModel(models.Model):
	order_number = models.IntegerField()
	user_name = models.CharField(max_length=100)
	user_phone = models.CharField(max_length=100)
	user_address = models.CharField(max_length=150)
	user_mail = models.EmailField(max_length=100)
	order_id = models.ManyToManyField(Shoes)


class OrderAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'user_name', 'user_phone', 'user_address', 'user_mail']
	search_fields = ['order_number', 'user_name', 'user_phone', 'user_address']


admin.site.register(BasketModel, BasketAdmin)
admin.site.register(OrderModel, OrderAdmin)


