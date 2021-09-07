import environ

from django.utils.translation import gettext_lazy as _
from pathlib import Path

# django-environ

env = environ.Env()

env.read_env('.env')

# Base settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('SECRET_KEY')

DEBUG = env.get_value('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'django_filters',
    'django_hosts',
    'corsheaders',
    'main',
    'api',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database

DATABASES = {
    'default': env.db(),
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('ja', _('Japanese')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = 'static/'

STATIC_URL = '/static/'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging

LOG_DIR = BASE_DIR.parent / 'logs/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(message)s %(pathname)s:%(lineno)d',
        },
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'info.log',
            'formatter': 'production',
            'maxBytes': 500000,
            'backupCount': 5,
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'warning.log',
            'formatter': 'production',
            'maxBytes': 500000,
            'backupCount': 5,
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'error.log',
            'formatter': 'production',
            'maxBytes': 500000,
            'backupCount': 5,
        },
    },
    'root': {
        'handlers': ['info', 'warning', 'error'],
        'level': 'INFO',
    }
}


# API Authentication

API_AUTH_USER_MODEL = 'main.User'


# AWS Cognito

COGNITO_AWS_REGION = 'ap-northeast-1'

COGNITO_USER_POOL = 'ap-northeast-1_Qmhnf71Gf'

COGNITO_AUDIENCE = env('COGNITO_AUDIENCE')


# Django rest framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.CognitoAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'api.pagenations.CursorPagination'
}


# django-hosts

DEFAULT_HOST = 'api'

ROOT_HOSTCONF = 'project.urls'


# django cors headers

CORS_ALLOW_ALL_ORIGINS = DEBUG

CORS_ALLOWED_ORIGINS  =  []

