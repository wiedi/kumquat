from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^status/$', 'status.views.status', name='status'),
	url(r'^system/', include('kumquat.urls')),
	url(r'^ftp/',    include('ftp.urls')),
	url(r'^mysql/',  include('mysql.urls')),
	url(r'^web/',    include('web.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
