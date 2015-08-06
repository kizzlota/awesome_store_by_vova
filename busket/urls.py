from django.conf.urls import url

urlpatterns = [
	url(r'^new/', 'busket.views.new_order', name='new_order'),
	url(r'^new_test/', 'busket.views.new_order', name='new_order'),
	url(r'^find/', 'busket.views.finded_orders', name='finded_orders'),
	url(r'^list_all_orders/', 'busket.views.list_orders', name='list_orders'),
	url(r'^order_detail/', 'busket.views.order_detail', name='order_detail'),
	url(r'^edit_shoe_quantity/', 'busket.views.edit_shoe_quantity', name='edit_shoe_quantity'),
	url(r'^del_from_order/(?P<order_id>\d+)/(?P<shoe_id>\d+)/$', 'busket.views.del_from_order', name='del_from_order'),
]
