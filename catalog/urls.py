from django.conf.urls import url


urlpatterns = [
	url(r'^$', 'catalog.views.index', name='index'),
	url(r'^news/', 'catalog.views.out_news', name='out_news'),
	url(r'^test/', 'catalog.views.gallerey', name='gallerey'),
	url(r'^busket/', 'catalog.views.busket', name='busket'),
	url(r'^busket_del/', 'catalog.views.busket_del', name='del_basket')


]