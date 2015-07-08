from django.forms import ModelForm
from models import User


class RegisterForm(ModelForm):
	class Meta:
		model = User
		fields = 'username', 'password', 'email'


class RegisterFormSecond(ModelForm):
	class Meta:
		model = User
		fields = 'first_name', 'last_name', 'user_bio'


