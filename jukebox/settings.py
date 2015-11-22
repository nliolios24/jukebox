"""
Django settings for jukepod project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, datetime
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "/../")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jc=jl@ckuf^k!l0gg#rvqj$ju5sx-1_ul(375dn*g$js95z8u)'

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

    # 3rd party
    'corsheaders',
    'rest_framework',
    'guardian',

    # Local
    'authentication',
    'pods',
    'songs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'corsheaders.middleware.CorsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'jukebox.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ), 
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_ALLOW_REFRESH': True,
}

AUTH_USER_MODEL = 'authentication.Account'

AUTHENTICATION_BACKENDS = (
    'authentication.backends.AccountAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

WSGI_APPLICATION = 'jukebox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if os.environ.get('DATABASE_URL'):
    from urlparse import urlparse
    _db_url = urlparse(os.environ.get('DATABASE_URL', ''))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': _db_url.path[1:],
            'USER': _db_url.username,
            'PASSWORD': _db_url.password,
            'HOST': _db_url.hostname,
            'PORT': _db_url.port,
        },
    }

else:
    db_user = get_env_setting('DB_USER')
    db_password = get_env_setting('DB_PASSWORD')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'jukebox',
            'USER': db_user,
            'PASSWORD': db_password,
            'HOST': 'localhost',
            'PORT': ''
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Guardian
ANONYMOUS_USER_ID = -1

# Pod permissions system
POD_HOST_PERMISSIONS = ['add_accounts', 'remove_accounts', 'change_account_permissions', 'manage_pod']
POD_MEMBER_PERMISSIONS = ['add_accounts']