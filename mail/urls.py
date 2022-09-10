from django.urls import re_path
from mail import views

urlpatterns = [
	re_path(r'^accounts/$',                   views.AccountList.as_view(),    name='mail_account_list'),
	re_path(r'^accounts/add$',                views.AccountCreate.as_view(),  name='mail_account_add'),
	re_path(r'^accounts/(?P<pk>\d+)/update$', views.AccountUpdate.as_view(),  name='mail_account_update'),
	re_path(r'^accounts/(?P<pk>\d+)/delete$', views.AccountDelete.as_view(),  name='mail_account_delete'),

	re_path(r'^redirect/$',                   views.RedirectList.as_view(),   name='mail_redirect_list'),
	re_path(r'^redirect/add$',                views.RedirectCreate.as_view(), name='mail_redirect_add'),
	re_path(r'^redirect/(?P<pk>\d+)/update$', views.RedirectUpdate.as_view(), name='mail_redirect_update'),
	re_path(r'^redirect/(?P<pk>\d+)/delete$', views.RedirectDelete.as_view(), name='mail_redirect_delete'),

	re_path(r'^export.json$', views.export, name='mail_export'),

]
