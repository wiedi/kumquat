from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
	url(r'^databases/$',                   views.DatabaseList.as_view(),   name='mysql_database_list'),
	url(r'^databases/add$',                views.DatabaseCreate.as_view(), name='mysql_database_add'),
	url(r'^databases/(?P<slug>[a-z0-9_]+)/update$', views.databaseUpdate,    name='mysql_database_update'),
	url(r'^databases/(?P<slug>[a-z0-9_]+)/delete$', views.databaseDelete,    name='mysql_database_delete'),
)