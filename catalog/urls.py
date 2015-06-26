from django.conf.urls import url


urlpatterns = [
	url(r'^$', 'catalog.views.index', name='index'),
	url(r'^news/', 'catalog.views.out_news', name='out_news'),
	url(r'^busket/', 'catalog.views.busket', name='busket'),
	url(r'^busket_del/', 'catalog.views.busket_del', name='del_basket'),
	url(r'^for_test/', 'busket.views.new_user_order', name='for_test'),
	url(r'^shoe_ind/(?P<shoe_id>\d+)/$', 'catalog.views.shoe', name='shoe'),
	url(r'^test_app/', 'testing_issues.views.testing', name='testing'),
	url(r'^registration/', 'catalog.views.registration', name='registration'),

]