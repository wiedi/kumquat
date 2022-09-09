from django.urls import re_path
from web import views

urlpatterns = [
	re_path(r'^vhost/$',                            views.VHostList.as_view(),     name='web_vhost_list'),
	re_path(r'^vhost/add$',                         views.VHostCreate.as_view(),   name='web_vhost_add'),
	re_path(r'^vhost/(?P<pk>\d+)/update$',          views.VHostUpdate.as_view(),   name='web_vhost_update'),
	re_path(r'^vhost/(?P<pk>\d+)/delete$',          views.VHostDelete.as_view(),   name='web_vhost_delete'),

	re_path(r'^vhost/(?P<pk>\d+)/catchall$',        views.vhostCatchallSet,        name='web_vhost_catchall_set'),
	re_path(r'^vhost/catchall/(?P<pk>\d+)/delete$', views.vhostCatchallDelete,     name='web_vhost_catchall_delete'),

	re_path(r'^vhost/(?P<pk>\d+)/errorlog$',        views.vhostErrorLogList,       name='web_vhost_errorlog_list'),

	re_path(r'^vhost/(?P<pk>\d+)/alias$',           views.vhostAliasList,       name='web_vhost_alias_list'),
	re_path(r'^vhost/(?P<pk>\d+)/alias/add$',       views.vhostAliasAdd,        name='web_vhost_alias_add'),
	re_path(r'^vhost/alias/(?P<pk>\d+)/delete$',    views.vhostAliasDelete,     name='web_vhost_alias_delete'),

	re_path(r'^vhost/(?P<pk>\d+)/snapshot$',        views.vhostSnapshotList,       name='web_vhost_snapshot_list'),
	re_path(r'^vhost/(?P<pk>\d+)/snapshot/add$',    views.vhostSnapshotCreate,     name='web_vhost_snapshot_add'),
#	re_path(r'^vhost/(?P<pk>\d+)/snapshot/(?P<name>[A-Za-z0-9_-]+)/download$', views.vhostSnapshotDownload, name='web_vhost_snapshot_download'),
	re_path(r'^vhost/(?P<pk>\d+)/snapshot/(?P<name>[A-Za-z0-9_-]+)/rollback$', views.vhostSnapshotRollback, name='web_vhost_snapshot_rollback'),
	re_path(r'^vhost/(?P<pk>\d+)/snapshot/(?P<name>[A-Za-z0-9_-]+)/delete$',   views.vhostSnapshotDelete,   name='web_vhost_snapshot_delete'),

	re_path(r'^sslcert/$',                          views.SSLCertList.as_view(),        name='web_sslcert_list'),
	re_path(r'^sslcert/expired/$',                  views.ExpiredSSLCertList.as_view(), name='web_sslcert_list_expired'),
	re_path(r'^sslcert/add$',                       views.sslcertCreate,                name='web_sslcert_add'),
	re_path(r'^sslcert/(?P<pk>\d+)/delete$',        views.SSLCertDelete.as_view(),      name='web_sslcert_delete'),
	re_path(r'^sslcert/expired/delete/$',           views.sslcertDeleteExpired,         name='web_sslcert_delete_expired'),
]
