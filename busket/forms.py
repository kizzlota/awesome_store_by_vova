from django.forms import ModelForm
from busket.models import OrderModel


class OrderForm(ModelForm):
	class Meta:
		model = OrderModel
		fields = '__all__'

