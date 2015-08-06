# -*- coding: utf-8 -*-
import hashlib
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core import signing
from models import Shoes, Category, ShoeParameters, ShoeSizeParams, ShoesPhotos
from busket.models import BasketModel
from profiles.forms import ShoeParametersForm, ShoeSizeParamsForm, ShoesPhotosForm
import re
from django.forms.models import modelformset_factory

# Create your views here.


def true_busket(request):
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get(
		'HTTP_USER_AGENT', 'chrome') + \
	            request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')
	return BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())


def basket_info(request):
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get(
		'HTTP_USER_AGENT', 'chrome') + \
	            request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')

	basket = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())
	total_sum = 0
	id_list = []

	for ids in basket:
		id_list.append(ids.shoes_id.id)

	for ordering in basket:
		for price in ordering.shoes_id.shoeparameters_set.all():
			total_sum += price.price

	return basket, total_sum, id_list


def index(request):
	filter_for_price = False

	if request.GET.get('price') == 'price_big':
		filter_for_price = '-relation_to_shoes_params__price'

	if request.GET.get('price') == 'price_small':
		filter_for_price = 'relation_to_shoes_params__price'

	category = request.GET.get('c')

	if not category and not filter_for_price:
		shoes = Shoes.objects.all()
	elif filter_for_price:
		shoes = Shoes.objects.all().order_by(filter_for_price).distinct()

	elif filter_for_price and category:
		category = request.GET.get('c', u'Жіноче')
		shoes = Shoes.objects.filter(category_name__name=category).order_by(filter_for_price).distinct()

	else:
		category = request.GET.get('c', u'Жіноче')
		shoes = Shoes.objects.filter(category_name__name=category).order_by('-id')

	list_category = Category.objects.all()
	bought_cook = False
	if 'if_shoe_bought' in request.COOKIES:
		bought_cook = True
	asd = render(request, 'catalog/index.html',
	             {'category': list_category, 'shoes': shoes, 'basket': basket_info(request),
	              'bought_cook': bought_cook})
	# asd.set_cookie('favarite_color', 'red', max_age=8000)  # setting index cookie , not reasonable
	return asd


def shoe(request, shoe_id, params_id):
	indiv_shoe = Shoes.objects.get(id=shoe_id)
	ImageFormSet = modelformset_factory(ShoesPhotos, fields=('images',), extra=9)
	if request.method == 'POST':
		if request.POST.get('add_shoe'):
			form_pictures = ImageFormSet(request.POST, request.FILES)
			shoes_size_form = ShoeSizeParamsForm(request.POST)
			shoe_main_param = ShoeParametersForm(request.POST, request.FILES)

			if form_pictures.is_valid() and shoes_size_form.is_valid() \
					and shoe_main_param.is_valid():
				pictures_list = []

				if form_pictures.is_valid():
					data = form_pictures.save()
					for i in data:
						pictures_list.append(str(i))
				print pictures_list

				if shoes_size_form.is_valid():
					data1 = shoes_size_form.save(commit=False)
					data1.save()

				shoe_main_param = ShoeParametersForm(request.POST, request.FILES)
				if shoe_main_param.is_valid():
					data2 = shoe_main_param.save(commit=False)
					data2.save()
					data2.relation_to_shoes_photos = pictures_list
					data2.rel_to_size = [str(data1.id)]
					shoe_main_param.save_m2m()

					indiv_shoe.relation_to_shoes_params.add(ShoeParameters.objects.get(id=data2.id))
					indiv_shoe.save()

		if request.POST.get('add_size'):
			shoes_size_form = ShoeSizeParamsForm(request.POST)

			if shoes_size_form.is_valid():
				data1 = shoes_size_form.save(commit=False)
				data1.save()
				data_params = ShoeParameters.objects.get(id=params_id)
				data_params.rel_to_size.add(ShoeSizeParams.objects.get(id=data1.id))
				data_params.save()

		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form_pictures = ImageFormSet(queryset=ShoesPhotos.objects.none())  # pictures
		shoes_size_form = ShoeSizeParamsForm()
		shoe_main_param = ShoeParametersForm()

	return render(request, 'catalog/shoe_individual.html', {'indiv_shoe': indiv_shoe,
	                                                        'basket': basket_info(request),
	                                                        'params_id': int(params_id),
	                                                        'form_pictures': form_pictures,
	                                                        'shoes_size_form': shoes_size_form,
	                                                        'shoe_main_param': shoe_main_param
	                                                        })


def out_news(request):
	shoes_news = Shoes.objects.all().order_by('date')
	return render_to_response('catalog/news.html', {'outline_news': shoes_news, 'category': Category.objects.all()})


def busket(request):
	id0 = request.GET.get('id')
	shoe_size = ShoeSizeParams.objects.get(id=id0)

	id1 = request.GET.get('id', '1')  # if peyxodyt NOne to po default vstanovyt 1
	id2 = request.META.get('HTTP_REFERER')
	user_date = request.META.get('USERNAME', 'anonymous') + request.META.get('REMOTE_ADDR', 'host') + request.META.get(
		'HTTP_USER_AGENT', 'chrome') + request.META.get('PROCESSOR_IDENTIFIER', 'not_atested')
	# shoes = ShoeParameters.objects.get(id=id1)
	date = BasketModel(data_user_hash=hashlib.sha256(user_date).hexdigest(), quantity=1, shoes_id=shoe_size)
	date.save()
	asd = redirect(id2)  # HttpResponse
	asd.set_cookie('if_shoe_bought', max_age=3)
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


def simple_search(request):
	shoes_search = {}
	list_category = Category.objects.all()
	if request.method == 'GET':
		data = request.GET.get('search')
		shoes_search = ShoeParameters.objects.filter(Q(model_of_shoe=data) | Q(main_image__startswith=data) |
		                                             Q(shoes__id__startswith=data) | Q(material__startswith=data) |
		                                             Q(price__startswith=data) | Q(
			shoes__category_name__name=data)).distinct()
	return render(request, 'catalog/search_result.html', {'shoes_search': shoes_search, 'category': list_category,
	                                                      'basket': true_busket(request)})


def shoe_ind_edit(request, shoe_id, params_id):
	instance = get_object_or_404(ShoeParameters, id=params_id)
	indiv_shoe = Shoes.objects.get(id=shoe_id)
	ImageFormSet = modelformset_factory(ShoesPhotos, fields=('images',))
	if request.method == 'POST':
		if request.POST.get('add_shoe'):
			form_pictures = ImageFormSet(request.POST, request.FILES)
			shoes_size_form = ShoeSizeParamsForm(request.POST)
			shoe_main_param = ShoeParametersForm(request.POST, request.FILES, instance=instance)

			if shoe_main_param.is_valid() and form_pictures.is_valid():
				pictures_list = []
				#
				if form_pictures.is_valid():
					form_pictures.save()
				# data = form_pictures.save()
				# 	for i in data:
				# 		pictures_list.append(str(i))
				# print pictures_list
				#
				if shoes_size_form.is_valid():
					data1 = shoes_size_form.save(commit=False)
					data1.save()

				if shoe_main_param.is_valid():
					shoe_main_param.save()

		if request.POST.get('add_size'):
			shoes_size_form = ShoeSizeParamsForm(request.POST)

			if shoes_size_form.is_valid():
				data1 = shoes_size_form.save(commit=False)
				data1.save()
				data_params = ShoeParameters.objects.get(id=params_id)
				data_params.rel_to_size.add(ShoeSizeParams.objects.get(id=data1.id))
				data_params.save()

		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form_pictures = ImageFormSet(queryset=ShoesPhotos.objects.filter(shoeparameters__id=params_id))  # pictures
		shoes_size_form = ShoeSizeParamsForm()
		shoe_main_param = ShoeParametersForm(instance=instance)

	return render(request, 'catalog/shoe_individual_edit.html', {'indiv_shoe': indiv_shoe,
	                                                             'basket': basket_info(request),
	                                                             'params_id': int(params_id),
	                                                             'form_pictures': form_pictures,
	                                                             'shoes_size_form': shoes_size_form,
	                                                             'shoe_main_param': shoe_main_param
	                                                             })


URL = "https://api.telegram.org/bot%s/" % '120000427:AAGVzPumYWYHJAx_EtBS3KehPA2r-_5Fxwg'
