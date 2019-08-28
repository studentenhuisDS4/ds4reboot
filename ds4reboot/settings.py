"""
Django settings for ds4reboot project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import datetime
import os

from django.utils.timezone import now

from ds4reboot.secret_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from ds4reboot.utils import slashify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'user.apps.UserConfig',
    'bierlijst.apps.BierlijstConfig',
    'eetlijst.apps.EetlijstConfig',
    'thesau.apps.ThesauConfig',
    'organisation.apps.OrganisationConfig',
    'ds4admin.apps.Ds4AdminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'plugins',

    # API/ Angular
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'url_filter',

    # Wiki
    'django.contrib.sites.apps.SitesConfig',
    'django.contrib.humanize.apps.HumanizeConfig',
    'django_nyt.apps.DjangoNytConfig',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki.apps.WikiConfig',
    'wiki.plugins.attachments.apps.AttachmentsConfig',
    'wiki.plugins.notifications.apps.NotificationsConfig',
    'wiki.plugins.images.apps.ImagesConfig',
    'wiki.plugins.macros.apps.MacrosConfig',
]

INSTALLED_APPS += SECRET_APPS

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ds4reboot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "sekizai.context_processors.sekizai",
            ],
        },
    },
]

# Production
WSGI_APPLICATION = 'ds4reboot.wsgi.application'

AUTHENTICATION_BACKENDS = ['ds4reboot.auth.EmailorUsernameModelBackend']

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]
APPEND_SLASH = True
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'url_filter.integrations.drf.DjangoFilterBackend',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'EXCEPTION_HANDLER': 'ds4reboot.apps.common.drf.exception_handler',
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=3),
}

API_BASE_URL = 'api/v1/'

# Frontend CORS
# https://github.com/ottoyiu/django-cors-headers/#configuration
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "https://app.ds4.nl",
    "http://localhost:4200",
]

CSRF_TRUSTED_ORIGINS = [
    'ds4.nl',
]

# Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = True  # Use local time

# Generated uploads
HR_REPORTS_FOLDER = 'hr_reports/'
AVATAR_FOLDER = 'avatars/'
RECEIPTS_FOLDER = 'receipts/'
TEMP_FOLDER = 'temp/'

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'
MEDIA_URL = '/media/'
if DEBUG:
    # The final slash fucks up file upload...
    MEDIA_ROOT = './media'
else:
    MEDIA_ROOT = '/var/www/media/'

if DEBUG and not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT + '/')
if not os.path.exists(slashify(MEDIA_ROOT) + TEMP_FOLDER):
    os.mkdir(slashify(MEDIA_ROOT) + TEMP_FOLDER)
if not os.path.exists(slashify(MEDIA_ROOT) + HR_REPORTS_FOLDER):
    os.mkdir(slashify(MEDIA_ROOT) + HR_REPORTS_FOLDER)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Wiki part
WIKI_ACCOUNT_HANDLING = True
WIKI_ACCOUNT_SIGNUP_ALLOWED = True
SITE_ID = 1

# Attachments
DELETE_ATTACHMENTS_FROM_DISK = False
FILE_UPLOAD_MAX_SIZE = 3024000  # ~3MB

SILENCED_SYSTEM_CHECKS = ["rest_framework.W001"]

LOG_FOLDER = 'log'
if not os.path.exists(slashify(MEDIA_ROOT) + LOG_FOLDER):
    print('Created log folder')
    os.mkdir(slashify(MEDIA_ROOT) + LOG_FOLDER)
ADMINS = [('David', 'davidzwa@gmail.com')]
MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'filename': slashify(MEDIA_ROOT) + LOG_FOLDER + '/debug.log',
            'formatter': 'verbose'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console', 'mail_admins'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    }
}

if DEBUG and os.environ.get('RUN_MAIN', None) != 'true':
    LOGGING = {}
