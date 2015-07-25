from django.conf.urls import url

urlpatterns = [
    # url(r'^shoe_ind/(?P<shoe_id>\d+)/$', 'catalog.views.shoe', name='shoe'),
    # url(r'^test_app/', 'testing_issues.views.testing', name='testing'),
    url(r'^registration/', 'profiles.views.registration', name='registration'),
    url(r'^secondstep/', 'profiles.views.registration_second', name='registration_second'),
    url(r'^verify/', 'profiles.views.verify', name='verify'),
    url(r'^login/', 'profiles.views.user_login', name='user_login'),
    url(r'^logout/$', 'profiles.views.user_logout', name='logout'),
    url(r'^cabinet/', 'profiles.views.cabinet', name='cabinet'),
    url(r'^list_orders/', 'profiles.views.list_orders', name='list_orders'),
    url(r'^list_orders/', 'profiles.views.list_orders', name='list_orders'),
    url(r'^manager/', 'profiles.views.manager', name='manager'),

]
