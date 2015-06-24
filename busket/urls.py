from django.conf.urls import url

urlpatterns = [
	url(r'^new/', 'busket.views.new_order', name='new_order'),
	url(r'^new_test/', 'busket.views.new_order', name='new_order'),
	url(r'^find/', 'busket.views.finded_orders', name='finded_orders'),

]
