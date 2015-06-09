from django.conf.urls import url

urlpatterns = [
	url(r'^new/', 'busket.views.new_order', name='new_order'),

]
