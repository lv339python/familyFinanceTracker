"""
Django settings for iBudget project.


For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%b@ng!87zw9hwqy^xh75xpck^w1gj#0o*kdks#wtrnhr!xmeuv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'fund',
    'group',
    'income',
    'income_history',
    'spending',
    'spending_history',
    'webpack_loader',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_COOKIE_HTTPONLY = False

AUTH_USER_MODEL = 'authentication.UserProfile'

ROOT_URLCONF = 'ibudget.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'static/public')],
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

WSGI_APPLICATION = 'ibudget.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_USER_PASSWORD',
        'HOST': 'HOST',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/public/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public')

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static/public'),
)

WEBPACK_LOADER = {
  'DEFAULT': {
    'CACHE': not DEBUG,
    'BUNDLE_DIR_NAME': '',
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    'POLL_INTERVAL': 0.1,
    'TIMEOUT': None,
    'IGNORE': ['.+\.hot-update.js', '.+\.map']
  }
}

CLIENT_ID = '1086962473724-39bt35f7knvd6ef704qd2regsm1g5a4m.apps.googleusercontent.com'
CLIENT_SECRET = 'UZZnoAzCT7FbE_WsLjfkant0'
REDIRECT_URL = 'http://localhost:8000/api/v1/authentication/sign_in'
SCOPE = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
LOCAL_URL = "http://127.0.0.1:8000"

# AWS

AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'

AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'

AWS_STORAGE_BUCKET_NAME = 'AWS_STORAGE_BUCKET_NAME'




try:
    from .local_settings import *
except ImportError:
    print('Unable to load local_settings.py:')
