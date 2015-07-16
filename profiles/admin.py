from django.contrib import admin
from models import RegistrationCode
from django.contrib.auth.admin import UserAdmin
from models import User, UserAddress

# Register your models here.
class RegistrationCodeAdmin(admin.ModelAdmin):
	list_display = ['code', 'username', 'date']


class AuthUserAdmin(UserAdmin):
		list_display = ('username', 'email', 'is_staff', 'is_superuser')
		list_filter = ('is_superuser',)

		fieldsets = (
			(None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name',
			                   'social_img_url', 'profile_image', 'user_details', 'user_bio', 'last_login', 'date_joined')}),
			('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
		)

		add_fieldsets = (
			(None, {
				'classes': ('wide',),
				'fields': ('username', 'email', 'password1', 'password2', 'user_details',  'is_staff', 'is_superuser')}
			 ),
		)

		search_fields = ('username', 'email')
		ordering = ('username',)
		filter_horizontal = ('groups', 'user_permissions',)

class UserAddressAdmin(admin.ModelAdmin):
	list_display = ('id', 'phone', 'address', 'city', 'street', 'country')


admin.site.register(User, AuthUserAdmin)
admin.site.register(RegistrationCode, RegistrationCodeAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
