"""
Django settings for the gunsiano project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Local configuration

from local_settings import DEBUG, SECRET_KEY, DATABASES

TEMPLATE_DEBUG = DEBUG


# Security

ALLOWED_HOSTS = ['*']


# Administration

ADMINS = [('Katherine Erickson', 'katherine.erickson@gmail.com'),]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'jquery',

    'universal',
    'website',
    'worm_strains',
    'vectors',
    'storage',
    'protocols',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gunsiano.urls'

WSGI_APPLICATION = 'gunsiano.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'staticfiles'


# For request object in templates

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


# Login

LOGIN_URL = 'login_url'
LOGIN_REDIRECT_URL = 'home_url'


# Markdown prompt for Admin

MARKDOWN_PROMPT = (
    'Use Markdown syntax for italics, bullets, etc. See '
    '<a href="http://www.darkcoding.net/software/markdown-quick-reference">'
    'a quick reference</a>, '
    '<a href="http://www.markdowntutorial.com/">a tutorial</a>, '
    'or practice <a href="http://dillinger.io/">here</a>. '
    'For subscripts: H~2~0. '
    'For superscripts: 6.02 x 10^23^.'
)
