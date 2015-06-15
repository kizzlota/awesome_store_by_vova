# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import OrderModel, Shoes
from django.shortcuts import render_to_response
from photologue.models import Gallery
import hashlib
from busket.models import BasketModel
from django.shortcuts import redirect
from forms import OrderForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect


def new_order(request):

	orders = OrderModel.objects.all()
	user_date = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
	            request.META.get('PROCESSOR_IDENTIFIER')
	basket = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())
	i_all = 0
	for ord in orders:
		for i in ord.order_id.all():
			i_all += i.price

	if request.method == 'POST':                    # якщо метод з форми є POST тоді наступне
		name_form = OrderForm(request.POST)         # свторюємо PostForm з даними з форми
		if name_form.is_valid():                    # валідація
			post = name_form.save(commit=False)     # відтермінування збереження форми комміт=фолс
			post.save()                             # saving and redirecting
			name_form.save_m2m()
			return HttpResponseRedirect('/')
	else:
		name_form = OrderForm()

	return render(request, 'orders/orders.html', {'orders_outlines': orders, 'full_price': i_all, 'user_info': name_form, 'basket_info': basket})


def new_user_order(request):
	form = OrderForm()

	user_data = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
	            request.META.get('PROCESSOR_IDENTIFIER')
	basket_hash = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_data).hexdigest())

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			post = form.save()
			post.save()
			return redirect('/')
	asd = OrderModel.objects.filter(id=11)
	frg = OrderModel.objects.all()

	return render(request, 'catalog/for_test.html', {'basket_info_test': basket_hash, 'form': form, 'asd': asd, 'frg': frg})
