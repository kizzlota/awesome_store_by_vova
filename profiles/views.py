# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from catalog.models import Category, Shoes, ShoeParameters, ShoesPhotos, ShoeSizeParams
from models import User, UserAddress, RegistrationCode
from forms import RegisterForm, RegisterFormSecond, ShoesForm, ShoeParametersForm, ShoeSizeParamsForm, ShoesPhotosForm
from profiles.mailing import send_email
from busket.models import OrderModel
from django.db.models import Sum

from catalog.views import basket_info


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

            return HttpResponseRedirect('/profiles/secondstep/')
    else:
        reg_form = RegisterForm()
    return render(request, 'profiles/registration.html',
                  {'category': list_category, 'reg_form': reg_form, 'registration': True,
                   'basket': basket_info(request)})


@login_required
def registration_second(request):
    if request.user.is_authenticated():
        if not request.user.is_active:
            if request.method == 'POST':
                reg_form_sec = RegisterFormSecond(data=request.POST, instance=request.user)
                if reg_form_sec.is_valid():
                    user = reg_form_sec.save(commit=False)
                    user_address = UserAddress(phone=reg_form_sec.cleaned_data.get('phone'),
                                               address=reg_form_sec.cleaned_data.get('address'))
                    user_address.save()
                    user.user_details = user_address
                    user.save()

                    return HttpResponseRedirect('/profiles/cabinet/')
            else:
                second_form = RegisterFormSecond()

            return render(request, 'profiles/registration.html', {'second_form': second_form, 'second': True})
        else:
            return render(request, 'errors/500.html')


def verify(request):
    code = request.GET.get('code')


# замути тут перевірку і активацію користувача .




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


def cabinet(request):
    return render(request, 'profiles/user_cabinet.html', {})


def list_orders(request):
    user = request.user.username
    obj_orders = OrderModel.objects.filter(user_name=user).annotate(total=Sum('order_id__price'))
    # print obj_orders[0].total
    # print obj_orders[1].total
    total_sum = OrderModel.objects.filter(user_name=user).aggregate(total=Sum('order_id__price'))

    return render(request, 'profiles/list_orders.html', {'obj_orders': obj_orders, 'total_sum': total_sum})


def manager(request):
    """method interact user as manager and renders manager's page """
    user_identity = request.user.username
    user_filter = request.user.is_staff
    if request.method == 'POST':
        pictures_list = []
        photo_form_set = ShoesPhotosForm(request.POST)
        if photo_form_set.is_valid():
            data = photo_form_set.save(commit=False)
            data.save()
            pictures_list.append(str(data.id))
        print pictures_list

        shoe_param_set = ShoeSizeParamsForm(request.POST)
        if shoe_param_set.is_valid():
            data1 = shoe_param_set.save(commit=False)
            data1.save()

        true_post = dict(request.POST)
        request.POST = request.POST.copy().dict()
        request.POST['relation_to_shoes_photos'] = pictures_list
        request.POST['rel_to_size'] = [str(data1.id)]

        shoe_main_param = ShoeParametersForm(request.POST)
        if shoe_main_param.is_valid():
            data2 = shoe_main_param.save(commit=False)
            data2.save()
            shoe_main_param.save_m2m()

        request.POST['relation_to_shoes_params'] = [str(data2.id)]
        request.POST['category_name'] = true_post['category_name']

        shoe_main = ShoesForm(request.POST)
        if shoe_main.is_valid():
            data3 = shoe_main.save(commit=False)
            data3.save()
            shoe_main.save_m2m()

    else:
        photo_form_set = ShoesPhotosForm()  # pictures
        shoe_param_set = ShoeSizeParamsForm()
        shoe_main_param = ShoeParametersForm()
        shoe_main = ShoesForm()

    return render(request, 'profiles/managing.html',
                  {'photo_form_set': photo_form_set, 'shoe_param_set': shoe_param_set,
                   'shoe_main_param': shoe_main_param, 'shoe_main': shoe_main})
