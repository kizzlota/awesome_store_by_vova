from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from catalog.models import Category
from models import User
from forms import RegisterForm, RegisterFormSecond
from profiles.mailing import send_email
from busket.models import OrderModel
from django.db.models import Sum
# Create your views here.


def registration(request):
	list_category = Category.objects.all()
	if request.method == 'POST':
		id_user = request.POST.get('username')
		# print id_user
		# info_form = RegistrationCode.objects.get(username__username=id_user)
		# print info_form
		reg_form = RegisterForm(request.POST)
		if reg_form.is_valid():
			data = reg_form.cleaned_data
			user = User.objects.create_user(username=data['username'], email=data['email'])
			user.set_password(data['password'])
			# reg_form.save_m2m()
			user.save()
			loginuser = authenticate(username=data['username'], password=data['password'])
			login(request, loginuser)
			send_email(user, prefix='signup_email')

			return HttpResponseRedirect('profiles/secondstep/')
	else:
		reg_form = RegisterForm()
	return render(request, 'profiles/registration.html', {'category': list_category, 'reg_form': reg_form, 'registration': True})


def registration_second(request):
	if request.user.is_authenticated():
		if not request.user.is_active:
			if request.method == 'POST':
				reg_form_sec = RegisterFormSecond(data=request.POST, instance=request.user)
				if reg_form_sec.is_valid():
					user = reg_form_sec.save(commit=False)
					user.save()

					return HttpResponseRedirect('/profiles/')
			else:
				second_form = RegisterFormSecond()

			return render(request, 'profiles/registration.html', {'second_form': second_form, 'second': True})


def user_login(request):
	username = request.POST.get('your_username')
	password = request.POST.get('your_password')
	error_text = None
	if request.method == 'POST':
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			error_text = 'this data is not matching any records'

	return render(request, 'profiles/user_login.html', {'error_text': error_text})

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/')

def base_page(request):
	return render(request, 'base.html', context_instance=RequestContext(request))


def list_orders(request):
	'''
	method that makes view of previous orders, realized throe authentication
	'''
	if request.user.is_authenticated():
		if request.user.is_active:
			user = request.user.username
			obj_orders = OrderModel.objects.filter(user_name=user).annotate(total=Sum('order_id__price'))
			print obj_orders[0].total
			# print obj_orders[1].total
			total_sum = OrderModel.objects.filter(user_name=user).aggregate(total=Sum('order_id__price'))

	return render(request, 'profiles/list_orders.html', {'obj_orders': obj_orders, 'total_sum': total_sum})
