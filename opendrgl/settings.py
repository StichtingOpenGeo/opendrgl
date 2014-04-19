"""
Django settings for opendrgl project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6^=-1p_&hxt&p(_g&$)s%a0qod3+fvlcobvdrr=p$5%gc@(m&r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',

    'projects',
    'stops',
    'trips',

    # Libs
    'crispy_forms',
    'leaflet',

    # Admin & tools
    'south',
    'django_admin_bootstrapped',
    'django.contrib.admin'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'opendrgl.urls'

WSGI_APPLICATION = 'opendrgl.wsgi.application'

# Templates
TEMPLATE_DIRS = ("opendrgl/templates", )

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

LEAFLET_CONFIG = {
    'TILES': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'RESET_VIEW': False
}

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'opendrgl',
        'USER': 'opendrgl',
        'PASSWORD': 'opendrgl',
        'HOST': '127.0.0.1'
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

STATICFILES_DIRS = ("opendrgl/static",)