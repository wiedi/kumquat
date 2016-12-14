from django.conf.urls import url
from mail import views

urlpatterns = [
	url(r'^accounts/$',                   views.AccountList.as_view(),    name='mail_account_list'),
	url(r'^accounts/add$',                views.AccountCreate.as_view(),  name='mail_account_add'),
	url(r'^accounts/(?P<pk>\d+)/update$', views.AccountUpdate.as_view(),  name='mail_account_update'),
	url(r'^accounts/(?P<pk>\d+)/delete$', views.AccountDelete.as_view(),  name='mail_account_delete'),

	url(r'^redirect/$',                   views.RedirectList.as_view(),   name='mail_redirect_list'),
	url(r'^redirect/add$',                views.RedirectCreate.as_view(), name='mail_redirect_add'),
	url(r'^redirect/(?P<pk>\d+)/update$', views.RedirectUpdate.as_view(), name='mail_redirect_update'),
	url(r'^redirect/(?P<pk>\d+)/delete$', views.RedirectDelete.as_view(), name='mail_redirect_delete'),

	url(r'^export.json$', views.export, name='mail_export'),

]