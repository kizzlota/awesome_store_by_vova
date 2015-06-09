# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import OrderModel
from django.shortcuts import render_to_response
from photologue.models import Gallery
import hashlib
from busket.models import BasketModel
from django.shortcuts import redirect



def new_order(request):
	#id1 = request.GET.get('id')
	orders = OrderModel.objects.all()
	#date = BasketModel(data_user_hash=hashlib.sha256(user_date).hexdigest(), quantity=1, shoes_id=shoes)
	# date.data_user_hash = hashlib.sha256(user_date).hexdigit()
	# date.shoes_id = id1
	# date.quantity = 1
	#date.save()
	i_all = 0
	for ord in orders:
		for i in ord.order_id.all():
			i_all += i.price

	return render_to_response('orders/orders.html', {'orders_outlines': orders, 'full_price': i_all})




