from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from catalog.models import User


class AuthUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name',
                           'social_img_url', 'profile_image', 'user_bio', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, AuthUserAdmin)