from django.forms import ModelForm
from models import User
from catalog.models import Shoes, ShoeSizeParams, ShoesPhotos, ShoeParameters


class RegisterForm(ModelForm):
	class Meta:
		model = User
		fields = 'username', 'password', 'email'


class RegisterFormSecond(ModelForm):
	class Meta:
		model = User
		fields = 'first_name', 'last_name', 'user_bio'


class ShoesForm(ModelForm):
	class Meta:
		model = Shoes
		fields = 'manufacturer', 'name', 'description', 'category_name', 'relation_to_shoes_params'
		# exclude = 'relation_to_shoes_params',

class ShoeParametersForm(ModelForm):
	class Meta:
		model = ShoeParameters
		fields = 'model_of_shoe', 'color', 'date_manufac', 'price', 'new_price', 'material', 'vkladka', 'main_image', 'relation_to_shoes_photos', 'rel_to_size'
		# exclude = 'relation_to_shoes_photos', 'rel_to_size',

class ShoeSizeParamsForm(ModelForm):
	class Meta:
		model = ShoeSizeParams
		fields = 'size', 'height_shoe', 'height_heel', 'len_of_stelka', 'len_of_feet', 'quantity'

class ShoesPhotosForm(ModelForm):
	class Meta:
		model = ShoesPhotos
		fields = 'images',
