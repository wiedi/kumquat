from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
	url(r'^sslcert/$',                   views.SSLCertList.as_view(),   name='web_sslcert_list'),
	url(r'^sslcert/add$',                views.sslcertCreate,           name='web_sslcert_add'),
	url(r'^sslcert/(?P<pk>\d+)/delete$', views.SSLCertDelete.as_view(), name='web_sslcert_delete'),
)