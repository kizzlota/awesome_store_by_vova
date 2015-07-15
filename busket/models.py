from django.db import models
from django.contrib import admin
from catalog.models import Shoes, ShoeParameters
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json



# Create your models here.


class BasketModel(models.Model):
	data_user_hash = models.CharField(max_length=200)
	quantity = models.IntegerField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	shoes_id = models.ForeignKey(ShoeParameters)

	@property
	def info_mesht(self):
		return self.shoes_id


class BasketAdmin(admin.ModelAdmin):
	list_display = ["id", "data_user_hash", "quantity", "date", "shoes_id"]
	search_fields = ["data_user_hash", "date"]


class OrderModel(models.Model):
	user_name = models.CharField(max_length=100)
	user_phone = models.CharField(max_length=100)
	user_address = models.TextField(max_length=350)
	user_mail = models.EmailField(max_length=100)
	shoes_quantity = models.CharField(max_length=550, blank=True, null=True)
	order_id = models.ManyToManyField(ShoeParameters)
	#user_hash = models.CharField(blank=True, null=True, max_length=200)

	def save(self, *args, **kwargs):
		super(OrderModel, self).save(*args, **kwargs)
		self.test1()

	def test1(self):
		print 'true' + self.shoes_quantity
		x = self.shoes_quantity
		x = json.loads(x)
		for i, j in x.iteritems():
			id_in_shoes = ShoeParameters.objects.get(id=i)
			id_in_shoes.quantity -= int(j)
			id_in_shoes.save()
			print i, j

	# @receiver(post_save, sender=OrderModel)
	# def clear_busket_after(instance, **kwargs):
	#profile_hash = BasketModel.objects.filter()






class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'user_name', 'user_phone', 'user_address', 'user_mail']
	search_fields = ['user_name', 'user_phone', 'user_address']


# @receiver(models.signals.post_save, sender=OrderModel)
# def quantity_changer(sender, instance, **kwargs):
# 	print instance.shoes_quantity
# 	for i in instance.order_id.all():
# 		print i.id


admin.site.register(BasketModel, BasketAdmin)
admin.site.register(OrderModel, OrderAdmin)
