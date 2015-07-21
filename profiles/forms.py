from django import forms
from models import User, UserAddress
from catalog.models import Shoes, ShoeSizeParams, ShoesPhotos, ShoeParameters


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'username', 'password', 'email'


class RegisterFormSecond(forms.ModelForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name'
        exclude = ['user_details']

    def __init__(self, *args, **kwargs):
        super(RegisterFormSecond, self).__init__(*args, **kwargs)
        self.fields['phone'] = forms.CharField(max_length=25)
        self.fields['address'] = forms.CharField(widget = forms.Textarea(attrs={'cols': 30, 'rows': 5}))


class ShoesForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = 'manufacturer', 'name', 'description', 'category_name', 'relation_to_shoes_params'
    # exclude = 'relation_to_shoes_params',


class ShoeParametersForm(forms.ModelForm):
    class Meta:
        model = ShoeParameters
        fields = 'model_of_shoe', 'color', 'date_manufac', 'price', 'new_price', 'material', 'vkladka', 'main_image', 'relation_to_shoes_photos', 'rel_to_size'
    # exclude = 'relation_to_shoes_photos', 'rel_to_size',


class ShoeSizeParamsForm(forms.ModelForm):
    class Meta:
        model = ShoeSizeParams
        fields = 'size', 'height_shoe', 'height_heel', 'len_of_stelka', 'len_of_feet', 'quantity'


class ShoesPhotosForm(forms.ModelForm):
    class Meta:
        model = ShoesPhotos
        fields = 'images',
