# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import Shoes, Category
from django.shortcuts import render_to_response
from photologue.models import Gallery
import hashlib
from busket.models import BasketModel
from django.shortcuts import redirect
# Create your views here.


def index(request):
	category = request.GET.get('c', u'Чоботи')

	list_category = Category.objects.all()

	shoes = Shoes.objects.filter(category_name__name=category).order_by('-id')
	user_date = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
				request.META.get('PROCESSOR_IDENTIFIER')
	basket = BasketModel.objects.filter(data_user_hash=hashlib.sha256(user_date).hexdigest())

	return render(request, 'catalog/index.html', {'category': list_category, 'shoes': shoes, 'basket': basket})


def out_news(request):
	shoes_news = Shoes.objects.all().order_by('date')
	return render_to_response('catalog/news.html', {'outline_news': shoes_news, 'category': Category.objects.all()})


def gallerey(request):
	photo = Gallery.objects.all()
	print photo.__dict__
	return render_to_response('catalog/text.html', {'photos': photo})


def busket(request):
	id1 = request.GET.get('id')
	user_date = request.META.get('USERNAME') + request.META.get('REMOTE_ADDR') + request.META.get('HTTP_USER_AGENT') + \
				request.META.get('PROCESSOR_IDENTIFIER')
	shoes = Shoes.objects.get(id=id1)
	date = BasketModel(data_user_hash=hashlib.sha256(user_date).hexdigest(), quantity=1, shoes_id=shoes)
	# date.data_user_hash = hashlib.sha256(user_date).hexdigit()
	# date.shoes_id = id1
	# date.quantity = 1
	date.save()
	return redirect('/')


def busket_del(request):
	idl = request.GET.get('id')
	queryset = BasketModel.objects.filter(id=idl)
	queryset.delete()
	return redirect('/')





