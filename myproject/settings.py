#coding=utf-8
from __future__ import unicode_literals
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$of^55s=lv)p4vg^b+_l*wmlqm^*(o3$wg(#eyto_jxcevq#)m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG_TOOLBAR_PATCH_SETTINGS = False # show DEBUG TOOLBAR PANEL
ALLOWED_HOSTS = []

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'CRDB',
    'django.contrib.sites',
    'django_comments',
    'imagekit',
    'debug_toolbar',
    'djcelery',
    'HRONION',
    'djkombu',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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
                'django.core.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'NAME': 'myproject_database',
        'USER': 'atknin',
        'PASSWORD': 'vfntvfnbrf43',
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'HRONION.users'
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en-En'
#LANGUAGE_CODE = 'ru-RU'


USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
MEDIA_ROOT = '/opt/myenv/myproject/media/'
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/myenv/myproject/static/'

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER=False
CELERY_IGNORE_RESULT = True
CELERY_BACKEND_RESULT = 'amqp'
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"


# адрес redis сервера
BROKER_URL = 'redis://localhost:6379/0'
# храним результаты выполнения задач так же в redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# в течение какого срока храним результаты, после чего они удаляются
CELERY_TASK_RESULT_EXPIRES = 7*86400  # 7 days
# это нужно для мониторинга наших воркеров
CELERY_SEND_EVENTS = True
# место хранения периодических задач (данные для планировщика)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# в конец settings.py добавляем строчки
import djcelery
djcelery.setup_loader()

#почта 
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'atknin.ii@physics.msu.ru'
EMAIL_HOST_PASSWORD = 'Ghtpbltyn2030'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'atknin.ii@physics.msu.ru'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'