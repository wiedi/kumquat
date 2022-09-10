from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout_then_login
from status.views import status

admin.autodiscover()


urlpatterns = [
	re_path(r'^$',       status, name='status'),
	re_path(r'^system/', include('kumquat.urls')),
	re_path(r'^ftp/',    include('ftp.urls')),
	re_path(r'^mysql/',  include('mysql.urls')),
	re_path(r'^web/',    include('web.urls')),
	re_path(r'^mail/',   include('mail.urls')),
	re_path(r'^cron/',   include('cron.urls')),
	re_path(r'^admin/',  admin.site.urls),

	re_path(r'',         include('django.contrib.auth.urls')),

	re_path(r'^accounts/login/$',  auth_views.LoginView.as_view(), name='login'),
	re_path(r'^accounts/logout/$', logout_then_login, name='logout_then_login'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
