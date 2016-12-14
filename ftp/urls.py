from django.conf.urls import url
from ftp import views

urlpatterns = [
	url(r'^accounts/$',                   views.AccountList.as_view(),   name='ftp_account_list'),
	url(r'^accounts/add$',                views.AccountCreate.as_view(), name='ftp_account_add'),
	url(r'^accounts/(?P<pk>\d+)/update$', views.AccountUpdate.as_view(), name='ftp_account_update'),
	url(r'^accounts/(?P<pk>\d+)/delete$', views.AccountDelete.as_view(), name='ftp_account_delete'),
]