from django.urls import re_path
from kumquat import views

urlpatterns = [
	re_path(r'^domains/$',                   views.DomainList.as_view(),   name='domain_list'),
	re_path(r'^domains/add$',                views.DomainCreate.as_view(), name='domain_add'),
	re_path(r'^domains/(?P<pk>\d+)/delete$', views.DomainDelete.as_view(), name='domain_delete'),
]
