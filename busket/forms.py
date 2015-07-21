from django.forms import ModelForm
from busket.models import OrderModel


class OrderForm(ModelForm):
    class Meta:
        model = OrderModel
        fields = 'user_name', 'user_phone', 'user_address', 'user_mail', 'shoes_quantity'
