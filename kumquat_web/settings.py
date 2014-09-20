"""
Django settings for kumquat_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys, os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^s7@cvx=$d)uvd75)u_p(w12zswl%**et1s2xys$wkq-sx($-d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
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
	'kumquat',
	'web',
	'mysql',
	'ftp',
	'status',
	'mail',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kumquat_web.urls'
WSGI_APPLICATION = 'kumquat_web.wsgi.application'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	},
	'kumquat_mysql': {
		'ENGINE':   'django.db.backends.mysql',
		'HOST':     '192.168.15.238',
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
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
			'datefmt': '%Y-%m-%dT%H:%M:%S',
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
			'datefmt': '%Y-%m-%dT%H:%M:%S',
		},
	},
	'handlers': {
		# Log to a text file that can be rotated by logrotate
		'logfile': {
			'class': 'logging.handlers.WatchedFileHandler',
			'filename': '/var/log/django/kumquat.log',
		},
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

KUMQUAT_CERT_PATH     = '/opt/local/etc/openssl/httpd/'
KUMQUAT_VHOST_CONFIG  = '/opt/local/etc/httpd/vhosts.conf'
KUMQUAT_VHOST_ROOT    = '/srv/www/'
KUMQUAT_VHOST_UID     = 501
KUMQUAT_VHOST_GID     = 12
KUMQUAT_USE_ZFS       = False
KUMQUAT_VHOST_DATASET = 'zones/9183a8f7-dfe9-42a2-b2f3-647e698b916c/data/www'
KUMQUAT_WEBSERVER_RELOAD = 'svcadm refresh apache'
CORE_MAIL_TOKEN       = 'Soop6hoog6fohheagif8'
