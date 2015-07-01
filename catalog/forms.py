from django.forms import ModelForm
from catalog.models import User


class RegisterForm(ModelForm):
	class Meta:
		model = User
		fields = 'username', 'password', 'email', 'first_name', 'last_name', 'social_img_url', 'profile_image', 'user_bio'


class RegisterFormSecond(ModelForm):
	class Meta:
		model = User
		fields = 'first_name', 'last_name', 'user_bio'
