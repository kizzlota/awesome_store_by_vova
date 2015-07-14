from django.contrib import admin
from models import Shoes, ShoesPhotos, ShoeParameters, ShoeSizeParams
from django.contrib.auth.admin import UserAdmin
# from profile.models import UserDict

@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'manufacturer']
	filter_horizontal = ('category_name',)

@admin.register(ShoeSizeParams)
class ShoeSizeParamsAdmin(admin.ModelAdmin):
	list_display = ['zise', 'quantity']

@admin.register(ShoeParameters)
class ShoeParametersAdmin(admin.ModelAdmin):
	list_display = ['id', 'color', 'model_of_shoe', 'date_manufac', 'relation_to_photo', 'main_image']

@admin.register(ShoesPhotos)
class ShoesPhotosAdmin(admin.ModelAdmin):
	list_display = ['id', 'images']

#
# admin.site.register(Shoes, ShoesAdmin)
# admin.site.register(ShoeParameters, ShoeParametersAdmin)
# admin.site.register(ShoesPhotos, ShoesPhotosAdmin)