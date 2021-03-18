"""
Django settings for mydrive project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^-wosgt*o#(_b&iz64=t5j67fl&pegexm2$jtg8hd)gb@g^5e&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [
    'localhost',
    'blendmehani.pythonanywhere.com',
    '192.168.0.100'
]

# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'dashboard.apps.DashboardConfig',
    'core.apps.CoreConfig',
    'material.admin',
    'material.admin.default',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

AUTH_USER_MODEL = 'accounts.User'
ROOT_URLCONF = 'mydrive.urls'

MATERIAL_ADMIN_SITE = {
    'HEADER': _('My Personal Drive administration'),
    'TITLE': _('My Personal Drive'),
    'FAVICON': 'images/logo.png',  # Admin site favicon (path to static should be specified)
    'MAIN_BG_COLOR': '#353a40',
    'MAIN_HOVER_COLOR': '#6c747e',
    'PROFILE_PICTURE': 'material/admin/images/login-logo-night.jpg',
    'PROFILE_BG': 'images/admin_profile_bg.png',
    'LOGIN_LOGO': 'material/admin/images/login-logo-night.jpg',
    'LOGOUT_BG': 'images/admin_bg.png',
    'SHOW_THEMES': False,
    'TRAY_REVERSE': False,
    'NAVBAR_REVERSE': False,
    'SHOW_COUNTS': True,
    'APP_ICONS': {'accounts': 'account_box', 'core': 'dns', 'dashboard': 'dashboard'},
    'MODEL_ICONS': {'requests': 'get_app', 'directory': 'folder', 'file': 'description', 'sharedfile': 'offline_share'}
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'mydrive.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Tirane'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'media')
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_files')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'contact.mypersonaldrive@gmail.com'
EMAIL_HOST_PASSWORD = '**********'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
