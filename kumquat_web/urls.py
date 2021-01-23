from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from status.views import status

admin.autodiscover()


urlpatterns = [
	url(r'^$',       status, name='status'),
	url(r'^system/', include('kumquat.urls')),
	url(r'^ftp/',    include('ftp.urls')),
	url(r'^mysql/',  include('mysql.urls')),
	url(r'^web/',    include('web.urls')),
	url(r'^mail/',   include('mail.urls')),
	url(r'^cron/',   include('cron.urls')),
	url(r'^admin/',  admin.site.urls),

	url(r'',         include('django.contrib.auth.urls')),

	url(r'^accounts/login/$',  auth_views.LoginView.as_view(), name='login'),
	url(r'^accounts/logout/$', logout_then_login, name='logout_then_login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
