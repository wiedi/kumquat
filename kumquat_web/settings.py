"""
Django settings for kumquat_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys, os
from django.conf import global_settings
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^s7@cvx=$d)uvd75)u_p(w12zswl%**et1s2xys$wkq-sx($-d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'bootstrap3',
	'messagegroups',
	'annoying',
	'kumquat',
	'web',
	'mysql',
	'ftp',
	'status',
	'mail',
	'cron',
)

MIDDLEWARE = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kumquat_web.urls'
WSGI_APPLICATION = 'kumquat_web.wsgi.application'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'APP_DIRS': True,
		'DIRS': [
			os.path.join(BASE_DIR, 'templates'),
		],
		'OPTIONS': {
			'debug': True,
			'context_processors': [
				'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.debug',
				'django.template.context_processors.i18n',
				'django.template.context_processors.media',
				'django.template.context_processors.static',
				'django.template.context_processors.tz',
				'django.contrib.messages.context_processors.messages',
				'django_settings_export.settings_export',
			],
		},
	},
]

BOOTSTRAP3 = {
	'jquery_url': '/static/jquery.min.js',
	'base_url': '/static/bootstrap/',
	'css_url': '/static/bootstrap/bootstrap.min.css',
	'theme_url': '/static/bootstrap/bootstrap-theme.min.css',
	'javascript_url': '/static/bootstrap/bootstrap.min.js',
	'include_jquery': True,
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	},
	'kumquat_mysql': {
		'ENGINE':   'django.db.backends.mysql',
		'HOST':     '127.0.0.1',
		'USER':     'root',
		'PASSWORD': 'qwe123',
	}

}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

LOGIN_REDIRECT_URL = '/'

# Logging
# https://docs.djangoproject.com/en/dev/topics/logging/
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		# Only use logging if debug is false and it's a production environment
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
			'datefmt': '%Y-%m-%dT%H:%M:%S',
		},
		'simple': {
			'format': '%(levelname)s %(message)s',
			'datefmt': '%Y-%m-%dT%H:%M:%S',
		},
	},
	'handlers': {
		# Log to stdout
		'console': {
			'class':'logging.StreamHandler',
			'stream': sys.stdout,
		},
		# Log to syslog because this is much cleaner than extra file
		'syslog': {
			'class': 'logging.handlers.SysLogHandler',
			'facility': 'local1',
			'address': ('127.0.0.1', 514),
			'formatter': 'simple',
		},
	},
	'loggers': {
		# Might as well log any errors anywhere else in Django
		'django': {
			'handlers': ['console', 'syslog'],
			'level': 'ERROR',
			'propagate': False,
		},
	},
}

# kumquat
KUMQUAT_SITE_NAME        = ''

KUMQUAT_BACKEND_SOCKET   = "ipc:///tmp/kumquat_backend"
KUMQUAT_CERT_PATH        = '/opt/local/etc/openssl/kumquat/'
KUMQUAT_VHOST_CONFIG     = '/opt/local/etc/httpd/vhosts.conf'
KUMQUAT_VHOST_ROOT       = '/srv/www/'
KUMQUAT_VHOST_ERROR_LOG  = '/srv/www/{vhost}/logs/error.log'
KUMQUAT_VHOST_UID        = 501
KUMQUAT_VHOST_GID        = 12
KUMQUAT_USE_ZFS          = True

# without 0rpc the management jobs will have to be called by a cronjob
# some features (like snapshots) will not be available
KUMQUAT_USE_0RPC         = True

KUMQUAT_VHOST_DATASET    = 'zones/9764b9e4-7848-4af0-be52-131affa2bbcb/data/www'
KUMQUAT_WEBSERVER_RELOAD = 'svcadm refresh apache'
KUMQUAT_WEBMAIL_URL      = ''
KUMQUAT_PHPMYADMIN_URL   = ''
KUMQUAT_CRONJOB_CMD      = ['sudo', '-u', 'www', 'crontab']
KUMQUAT_VHOST_POST_CREATE_CMD = None
KUMQUAT_VHOST_POST_DELETE_CMD = None
CORE_MAIL_TOKEN          = 'Soop6hoog6fohheagif8'

LETSENCRYPT_CERT_KEY_BITS = 4096
LETSENCRYPT_ACCT_KEY_BITS = 4096
LETSENCRYPT_ACME_SERVER  = 'https://acme-staging-v02.api.letsencrypt.org/directory'
LETSENCRYPT_ACME_FOLDER  = '/opt/letsencrypt/acme/.well-known/acme-challenge/'
LETSENCRYPT_STATE_FOLDER = '/opt/letsencrypt/state/'

# valid whitelist values are described at https://mail.core.io/api/
# set this to None (or leave it undefined) to whitelist the same domain as the account
#CORE_MAIL_WHITELIST   = "*"

# Allow the following variables in the template
SETTINGS_EXPORT = [
	'KUMQUAT_WEBMAIL_URL',
	'KUMQUAT_PHPMYADMIN_URL',
	'KUMQUAT_USE_ZFS',
	'KUMQUAT_USE_0RPC',
	'KUMQUAT_SITE_NAME',
]
