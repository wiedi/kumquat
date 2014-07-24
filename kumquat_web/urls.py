from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^system/', include('kumquat.urls')),
	url(r'^ftp/',    include('ftp.urls')),
	url(r'^mysql/',  include('mysql.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
