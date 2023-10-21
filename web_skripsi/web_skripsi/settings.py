"""
Django settings for web_skripsi project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import json
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = list(os.getenv('ALLOWED_HOST').replace('[','').replace(']','').replace('"','').split(','))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'skripsi_app',
    'mathfilters',
    # 'skripsi_app.apps.SkripsiAppConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_cleanup.apps.CleanupConfig',
    # dev mode only
    "whitenoise.runserver_nostatic",
    # "django.contrib.staticfiles",
    # gdrive storage
    'gdstorage',
    # 'django.core.validators',
    # 'FileExtensionValidator',


]


CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

CSRF_TRUSTED_ORIGINS = ['https://skripsi-tiub.xyz','http://localhost','http://localhost:80','http://127.0.0.1:8000']
X_FRAME_OPTIONS = 'SAMEORIGIN'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # 'corsheaders.middleware.CorsMiddleware',,
]

ROOT_URLCONF = 'web_skripsi.urls'

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

WSGI_APPLICATION = 'web_skripsi.wsgi.application'
# WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }




# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': os.getenv('DATABASE_ACCOUNT_NAME'),
#     'USER':  os.getenv('DATABASE_ACCOUNT_USER'),
#     'PASSWORD': os.getenv('DATABASE_ACCOUNT_PASSWORD'),
#     'HOST': os.getenv('DATABASE_ACCOUNT_HOST'),
#     'PORT': '5432',
#   }
# }

# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.getenv('DATABASE_ACCOUNT_NAME'),
    'USER':  os.getenv('DATABASE_ACCOUNT_USER'),
    'PASSWORD': os.getenv('DATABASE_ACCOUNT_PASSWORD'),
    'HOST': os.getenv('DATABASE_ACCOUNT_HOST'),
    'PORT': '5432',
    'OPTIONS': {
            'sslmode': 'require',
        }
  }
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

# AUTH_USER_MODEL = 'skripsi_app.CustomUser'

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

# EMAIL handler
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'id'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Jakarta'

# USE_I18N = True
USE_L10N=False
# TIME_INPUT_FORMATS=('%H:%M',)
# TIME_INPUT_FORMATS = ['%H:%M:%S',]
# DATETIME_INPUT_FORMATS = ['%Y-%m-%d %H:%M:%S']
# TIME_FORMAT = 'h:i A'
# DATETIME_FORMAT = 'm/d/Y H:i:s'
# DATE_FORMAT = 'm/d/Y'
# TIME_INPUT_FORMATS=['%I:%M %p']

USE_TZ = False



# Locate your own json file in same directory as manage.py
# alternative : GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = os.path.join(BASE_DIR,'credentials.json')
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
# GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = 'json_drive_key.json'
# json_file=json.dumps()
GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS = os.getenv('GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS')
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT =   'media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_DIRS = os.path.join(BASE_DIR, 'skripsi_app//templates/static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'skripsi_app\templates\static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
# /vercel/path0/web_skripsi/skripsi_app\templates\static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = "/home"
LOGOUT_REDIRECT_URL = "/login"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# CORS_ALLOWED_ORIGINS = [
# "http://127.0.0.1:5500",
# "https://project-manager-sanketp60.tiiny.site",
# "https://project-management-sanketp60.netlify.apps"
# ]
# handler403="skripsi_app.views.permission_denied"
handler404="helpers.views.handle_not_found"
handler500="helpers.views.handle_server_error"

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG:'alert-info',
    messages.INFO:'alert-info',
    messages.SUCCESS:'alert-success',
    messages.WARNING:'alert-warning',
    messages.ERROR:'alert-danger',
}
