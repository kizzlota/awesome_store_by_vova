from django.shortcuts import render
from .models import TestShoes
# Create your views here.
def testing(request):
	shoes = TestShoes.objects.filter(relation_to_test__relation_to_photos__image='red')
	for each in shoes:
		for i in each.relation_to_test.all():
			print i.color
