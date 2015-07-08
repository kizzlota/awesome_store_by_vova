# -*- coding: utf-8 -*-
import hashlib
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core import signing
from models import Shoes, Category
from busket.models import BasketModel
import re

# Create your views here.


def true_busket(request):
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get('HTTP_USER_AGENT', 'chrome') + \
	                request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')
	return BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())


def index(request):
	category = request.GET.get('c', u'one')
	list_category = Category.objects.all()
	shoes = Shoes.objects.filter(category_name__name=category).order_by('-id')
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get('HTTP_USER_AGENT', 'chrome') + \
	            request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')
	basket = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())
	id_list = []
	for ids in basket:
		id_list.append(ids.shoes_id.id)
	hoes = []
	if 'id_list_basket' in request.COOKIES:
		id_list_cook_true = signing.loads(request.COOKIES['id_list_basket'])
		hoes = Shoes.objects.filter(id__in=id_list_cook_true)  # filter ne vyvodyt odnalovi zna4ennia, id__in = vylorystovuetis dlia filtruvannia bagatiox zna4en lista
	asd = render(request, 'catalog/index.html', {'category': list_category, 'shoes': shoes, 'basket': basket, 'id_list': id_list, 'hoes': hoes})
	asd.set_cookie('favarite_color', 'red', max_age=8000)  # setting index cookie , not reasonable
	return asd


def out_news(request):
	shoes_news = Shoes.objects.all().order_by('date')
	return render_to_response('catalog/news.html', {'outline_news': shoes_news, 'category': Category.objects.all()})


def busket(request):
	id1 = request.GET.get('id', '1')  # if peyxodyt NOne to po default vstanovyt 1
	id2 = request.META.get('HTTP_REFERER')
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get(
		'HTTP_USER_AGENT', 'chrome') + request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')
	shoes = Shoes.objects.get(id=id1)
	date = BasketModel(data_user_hash=hashlib.sha256(user_date).hexdigest(), quantity=1, shoes_id=shoes)
	date.save()
	asd = redirect(id2)  # HttpResponse
	if not 'id_list_basket' in request.COOKIES:
		id_list = []
		id_list.append(id1)
		id_list_cook_true = signing.dumps(id_list)
	else:
		id_list_cook = signing.loads(request.COOKIES['id_list_basket'])
		id_list_cook.append(id1)
		id_list_cook_true = signing.dumps(id_list_cook)

	user_cookies_value = signing.dumps(id1)
	asd.set_cookie('id_list_basket', id_list_cook_true, max_age=8000)

	return asd


def busket_del(request):
	idl = request.GET.get('id')
	id2 = request.GET.get('idc')
	queryset = BasketModel.objects.filter(id=idl)
	queryset.delete()
	update_cookie = redirect(request.META.get('HTTP_REFERER'))
	if 'id_list_basket' in request.COOKIES and 'idc' in request.GET:
		id_list_cook = signing.loads(request.COOKIES['id_list_basket'])

		id_list_cook.remove(id2)
		id_list_cook_true = signing.dumps(id_list_cook)
		update_cookie.set_cookie('id_list_basket', id_list_cook_true, max_age=8000)

	return update_cookie

def shoe(request, shoe_id):
	images = Shoes.objects.filter(id=shoe_id)

	return render(request, 'catalog/shoe_individual.html', {'images_few': images, 'basket': true_busket(request)})


def simple_search(request):
	shoes_search = {}
	list_category = Category.objects.all()
	if request.method == 'GET':
		data = request.GET.get('search')
		shoes_search = Shoes.objects.filter(Q(name__startswith=data) | Q(price__startswith=data) | Q(category_name__name__startswith=data)).distinct()
	return render(request, 'catalog/search_result.html', {'shoes_search': shoes_search, 'category': list_category,
	                                                      'basket': true_busket(request)})