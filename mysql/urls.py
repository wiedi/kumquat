from django.urls import re_path
from mysql import views

urlpatterns = [
	re_path(r'^databases/$',                   views.DatabaseList.as_view(),   name='mysql_database_list'),
	re_path(r'^databases/add$',                views.DatabaseCreate.as_view(), name='mysql_database_add'),
	re_path(r'^databases/(?P<slug>[a-z0-9_]+)/update$', views.databaseUpdate,    name='mysql_database_update'),
	re_path(r'^databases/(?P<slug>[a-z0-9_]+)/delete$', views.databaseDelete,    name='mysql_database_delete'),
]
