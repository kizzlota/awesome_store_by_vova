# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Shoes, Category, ShoesPhotos
from django.shortcuts import render_to_response
import hashlib
from busket.models import BasketModel
from django.shortcuts import redirect
# Create your views here.


def true_busket(request):
	user_date = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
	            request.META.get('PROCESSOR_IDENTIFIER')
	return BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())


def index(request):
	category = request.GET.get('c', u'mans')
	list_category = Category.objects.all()
	shoes = Shoes.objects.filter(category_name__name=category).order_by('-id')
	user_date = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
	            request.META.get('PROCESSOR_IDENTIFIER')
	basket = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())
	id_list = []
	for ids in basket:
		id_list.append(ids.shoes_id.id)
	return render(request, 'catalog/index.html', {'category': list_category, 'shoes': shoes, 'basket': basket, 'id_list': id_list})


def out_news(request):
	shoes_news = Shoes.objects.all().order_by('date')
	return render_to_response('catalog/news.html', {'outline_news': shoes_news, 'category': Category.objects.all()})


def gallerey(request):
	photo = Gallery.objects.all()
	print photo.__dict__
	return render_to_response('catalog/text.html', {'photos': photo})


def busket(request):
	id1 = request.GET.get('id')
	id2 = request.META.get('HTTP_REFERER')
	user_date = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
	            request.META.get('PROCESSOR_IDENTIFIER')
	shoes = Shoes.objects.get(id=id1)
	date = BasketModel(data_user_hash=hashlib.sha256(user_date).hexdigest(), quantity=1, shoes_id=shoes)
	date.save()
	return redirect(id2)


def busket_del(request):
	idl = request.GET.get('id')
	queryset = BasketModel.objects.filter(id=idl)
	queryset.delete()
	return redirect(request.META.get('HTTP_REFERER'))


def shoe(request, shoe_id):
	images = Shoes.objects.filter(id=shoe_id)

	return render(request, 'catalog/shoe_individual.html', {'images_few': images, 'basket': true_busket(request)})
