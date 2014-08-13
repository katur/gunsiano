"""
Django settings for Gunsiano lab website.
"""
import os

try:
    from local_settings import DEBUG, SECRET_KEY, DATABASES, STATIC_ROOT
except Exception as e:
    DEBUG = False
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()
    STATIC_ROOT = 'staticfiles'

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Katherine Erickson', 'katherine.erickson@gmail.com'),
)

MANAGERS = ADMINS

LOGIN_URL = 'login_url'
LOGIN_REDIRECT_URL = 'home_url'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

# Static asset configuration
SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(SETTINGS_DIR, '..')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gunsiano.urls'

WSGI_APPLICATION = 'gunsiano.wsgi.application'

TEMPLATE_DIRS = (
    # Needed so overridden admin templates take precedence
    PROJECT_DIR + '/universal/templates/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    'south',

    'universal',
    'website',
    'worm_strains',
    'vectors',
    'storage',
    'protocols',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

MARKDOWN_PROMPT = (
    'Use Markdown syntax for italics, bullets, etc. See '
    '<a href="http://www.darkcoding.net/software/markdown-quick-reference">'
    'a quick reference</a>, '
    '<a href="http://www.markdowntutorial.com/">a tutorial</a>, '
    'or practice <a href="http://dillinger.io/">here</a>. '
    'For subscripts: H~2~0. '
    'For superscripts: 6.02 x 10^23^.'
)

# For request object in templates
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)
