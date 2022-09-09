from django.urls import re_path
from ftp import views

urlpatterns = [
	re_path(r'^accounts/$',                   views.AccountList.as_view(),   name='ftp_account_list'),
	re_path(r'^accounts/add$',                views.AccountCreate.as_view(), name='ftp_account_add'),
	re_path(r'^accounts/(?P<pk>\d+)/update$', views.AccountUpdate.as_view(), name='ftp_account_update'),
	re_path(r'^accounts/(?P<pk>\d+)/delete$', views.AccountDelete.as_view(), name='ftp_account_delete'),
]
