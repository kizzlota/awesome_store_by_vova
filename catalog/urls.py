from django.conf.urls import url


urlpatterns = [
	url(r'^$', 'catalog.views.index', name='index'),
	url(r'^news/', 'catalog.views.out_news', name='out_news'),
	url(r'^busket/', 'catalog.views.busket', name='busket'),
	url(r'^busket_del/', 'catalog.views.busket_del', name='del_basket'),
	#url(r'^for_test/', 'busket.views.new_user_order', name='for_test'),
	url(r'^shoe_ind/(?P<shoe_id>\d+)/(?P<params_id>\d+)/$', 'catalog.views.shoe', name='shoe'),
	# url(r'^test_app/', 'testing_issues.views.testing', name='testing'),
	# url(r'^registration/', 'catalog.views.registration', name='registration'),
	# url(r'^reg/second/', 'catalog.views.registration_second', name='registration_second'),
	# url(r'^new_user/', 'catalog.views.registration_new_user', name='registration_new_user'),
	# url(r'^login/', 'catalog.views.user_login', name='user_login'),
	# url(r'^logout/$', 'catalog.views.user_logout', name='logout'),
	url(r'^search/', 'catalog.views.simple_search', name='simple_search'),
	url(r'^filter/', 'catalog.views.simple_filter', name='simple_filter'),


]