# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import OrderModel, Shoes
from django.shortcuts import render_to_response
import hashlib
from busket.models import BasketModel
from profiles.models import User
from django.shortcuts import redirect
from forms import OrderForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.core import signing


def new_order(request):
	user_credentials = {}
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get(
		'HTTP_USER_AGENT', 'chrome') + request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')
	basket = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())
	i_all = 0
	for ordering in basket:
		for price in ordering.shoes_id.shoeparameters_set.all():
			i_all += price.price

	if request.method == 'POST':  # якщо метод з форми є POST тоді наступне
		name_form = OrderForm(request.POST)  # свторюємо PostForm з даними з форми
		if name_form.is_valid():  # валідація
			post = name_form.save(commit=False)  # відтермінування збереження форми комміт=фолс
			post.save()  # saving and redirecting
			name_form.save_m2m()
			basket.delete()
			return HttpResponseRedirect('/')
	elif request.user.is_authenticated() and request.user.is_active:
		user_credentials['username'] = request.user.username
		user_credentials['user_mail'] = request.user.email
		user_order = User.objects.get(username=request.user.username)
		user_credentials['phone'] = user_credentials.get(user_order.user_details.phone, 'none')
		user_credentials['address'] = user_credentials.get(user_order.user_details.address, 'none')

		print user_credentials
		name_form = OrderForm()
	else:
		name_form = OrderForm()

	return render(request, 'orders/orders.html',
	              {'full_price': i_all, 'user_info': name_form, 'basket': basket,
	                'user_credentials': user_credentials})


def finded_orders(request):
	if request.method == 'POST':
		form_mail = request.POST.get('email_user')
		objects_in_orders = OrderModel.objects.filter(user_mail=form_mail).annotate(total=Sum('order_id__price'))
		print objects_in_orders[0].total
		print objects_in_orders[1].total
		# https://docs.djangoproject.com/en/1.8/topics/db/aggregation/
		total_sum = OrderModel.objects.filter(user_mail=form_mail).aggregate(total=Sum('order_id__price'))

	return render(request, 'orders/find_all_orders.html',
	              {'users_list_orders': objects_in_orders, 'total_sum': total_sum})

#
# def new_user_order(request):
# 	if "basket_cook" in request.COOKIES:
# 		get_cookies = request.COOKIES['basket_cook']
# 		fotos = Shoes.objects.filter(name=get_cookies)
# 	return render(request, 'catalog/for_test.html', {'frg': get_cookies, 'fotos': fotos})
