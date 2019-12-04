"""
Django settings for openalerts project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '68lo#(_a4ow1b*v6%a3d*$m(s4=2b@x*4&xv23vj$y4zq*l^_k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bulma',
    'social_django',
    'webpush',

    # LOCAL
    'alerts',
    'management',
    'subscriptions',
    'rss',
    'public'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'openalerts.urls'

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

WSGI_APPLICATION = 'openalerts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_auth_presspass.backends.PressPassBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_auth_presspass.pipelines.link_organizations_to_session',
)

AUTHENTICATION_BACKENDS = SOCIAL_AUTH_AUTHENTICATION_BACKENDS

SOCIAL_AUTH_URL_NAMESPACE = 'auth'

SOCIAL_AUTH_PRESSPASS_KEY = os.getenv('PRESSPASS_CLIENT_ID')
# SOCIAL_AUTH_PRESSPASS_SECRET = "16d4fd82b708834e2f051ec8680275e725d8af263ce17ac9528c81ad"

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": os.getenv('VAPID_PUBLIC_KEY'),
    "VAPID_PRIVATE_KEY": os.getenv('VAPID_PRIVATE_KEY'),
    "VAPID_ADMIN_EMAIL": os.getenv('VAPID_ADMIN_EMAIL')
}

LOGIN_URL = "/management/login/"

PRESSPASS_URL = "http://dev.squarelet.com"

PROTOCOL_AND_HOST = "http://localhost:8000"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM = "noreply@outgoing.openalerts.org"

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", None)
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", None)
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", None)
CSRF_COOKIE_SAMESITE = None
