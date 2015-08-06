# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from catalog.models import Shoes, ShoeParameters, ShoeSizeParams
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json


# Create your models here.


class BasketModel(models.Model):
    data_user_hash = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    shoes_id = models.ForeignKey(ShoeSizeParams)

    @property
    def info_mesht(self):
        return self.shoes_id


class BasketAdmin(admin.ModelAdmin):
    list_display = ["id", "data_user_hash", "quantity", "date", "shoes_id"]
    search_fields = ["data_user_hash", "date"]


class OrderModel(models.Model):
    PROCESSING = u'обробка'
    SENT = u'відправлено'
    DELIVERED = u'доставлено'
    status_choices = ((PROCESSING, u'processing'),
                      (SENT, u'sent'),
                      (DELIVERED, u'delivered')
                      )
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=100)
    user_address = models.TextField(max_length=350)
    user_mail = models.EmailField(max_length=100)
    shoes_quantity = models.CharField(max_length=550, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default=PROCESSING)

    # user_hash = models.CharField(blank=True, null=True, max_length=200)

    def save(self, *args, **kwargs):
        super(OrderModel, self).save(*args, **kwargs)
        self.test1()

    def test1(self):
        dic_quantity = self.shoes_quantity
        dic_quantity = json.loads(dic_quantity)
        for i, j in dic_quantity.iteritems():
            id_in_shoes = ShoeSizeParams.objects.get(id=i)
            id_in_shoes.quantity -= int(j)
            id_in_shoes.save()

    def total(self):
        dic_quantity = self.shoes_quantity
        dic_quantity = json.loads(dic_quantity)
        total_sum = 0
        for i, j in dic_quantity.iteritems():
            id_in_shoes = ShoeSizeParams.objects.get(id=i)
            for item in id_in_shoes.shoeparameters_set.all():
                total_sum += item.price * int(j)
        return total_sum

    def shoe_size_id(self):
        dic_quantity_true = json.loads(self.shoes_quantity)
        shoes_list = []
        for k, v in dic_quantity_true.iteritems():
            shoes_list.append(ShoeSizeParams.objects.get(id=k))
        return shoes_list


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'user_phone', 'user_address', 'user_mail', 'date', 'status']
    search_fields = ['user_name', 'user_phone', 'user_address']

# @receiver(models.signals.post_save, sender=OrderModel)
# def quantity_changer(sender, instance, **kwargs):
# 	print instance
# shoes_quantity
# 	for i in instance.order_id.all():
# 		print i.id


admin.site.register(BasketModel, BasketAdmin)
admin.site.register(OrderModel, OrderAdmin)
