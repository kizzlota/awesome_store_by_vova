# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from models import OrderModel, Shoes
from profiles.models import User
from forms import OrderForm, EditOrderForm
from django.http import HttpResponseRedirect
from django.db.models import Sum
from catalog.views import basket_info
from profiles.mailing import send_email, send_order_email


def new_order(request):

	user_credentials = {}
	info_basket = basket_info(request)
	if request.method == 'POST':  # якщо метод з форми є POST тоді наступне
		name_form = OrderForm(request.POST)  # свторюємо PostForm з даними з форми
		if name_form.is_valid():  # валідація
			data = name_form.cleaned_data
			post = name_form.save(commit=False)  # відтермінування збереження форми комміт=фолс
			post.save()  # saving and redirecting
			# name_form.save_m2m()
			info_basket[0].delete()
			send_order_email(post.id, prefix='send_order_email')
			return HttpResponseRedirect('/')

	else:
		name_form = OrderForm()

	return render(request, 'orders/orders.html',
	              {'full_price': info_basket[1], 'user_info': name_form, 'basket': info_basket,
	               'user_credentials': user_credentials})


def finded_orders(request):
	if request.method == 'POST':
		form_mail = request.POST.get('email_user')
		# objects_in_orders = OrderModel.objects.filter(user_mail=form_mail).annotate(total=Sum('order_id__price'))
		objects_in_orders = OrderModel.objects.filter(user_mail=form_mail)
	# print objects_in_orders[0].total
	# print objects_in_orders[1].total
	# https://docs.djangoproject.com/en/1.8/topics/db/aggregation/
	# total_sum = OrderModel.objects.filter(user_mail=form_mail).aggregate(total=Sum('order_id__price'))

	return render(request, 'orders/find_all_orders.html',
	              {'users_list_orders': objects_in_orders})


#
# def new_user_order(request):
# 	if "basket_cook" in request.COOKIES:
# 		get_cookies = request.COOKIES['basket_cook']
# 		fotos = Shoes.objects.filter(name=get_cookies)
# 	return render(request, 'catalog/for_test.html', {'frg': get_cookies, 'fotos': fotos})
def list_orders(request):
	all_orders_info = OrderModel.objects.all().order_by('-id')

	return render(request, 'orders/list_orders.html', {'all_orders_info': all_orders_info})


def order_detail(request):
	user_data = request.GET.get('o')

	user_order_detail = OrderModel.objects.filter(id=user_data)
	instance = get_object_or_404(OrderModel, id=user_data)
	if request.method == 'POST':
		print '!!!!!!!'
		edit_form = EditOrderForm(request.POST or None, instance=instance)
		if edit_form.is_valid():
			data = edit_form.cleaned_data()
			post = edit_form.save(commit=False)
			post.save()
			edit_form.save_m2m()
			return HttpResponseRedirect("/")
	else:
		edit_form = EditOrderForm(request.POST or None, instance=instance)

	return render(request, 'orders/order_detail.html', {'user_order_detail': user_order_detail, 'edit_form': edit_form, 'user_data': user_data})
