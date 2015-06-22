from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', 'status.views.status', name='status'),
	url(r'^system/', include('kumquat.urls')),
	url(r'^ftp/',    include('ftp.urls')),
	url(r'^mysql/',  include('mysql.urls')),
	url(r'^web/',    include('web.urls')),
	url(r'^mail/',   include('mail.urls')),
	url(r'^cron/',   include('cron.urls')),
	url(r'^admin/', include(admin.site.urls)),

	url(r'', include('django.contrib.auth.urls')),

	url(r'^accounts/login/$',                'django.contrib.auth.views.login'),
	url(r'^accounts/logout/$',               'django.contrib.auth.views.logout_then_login'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
