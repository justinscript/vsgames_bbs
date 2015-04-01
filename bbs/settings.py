# coding=utf-8
"""
Django settings for bbs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3zq63re--h_w0!p!en)&1crd@q-4pkyb27&0pvy(@t3qvh_53('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'datas',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bbs.urls'

WSGI_APPLICATION = 'bbs.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'medias').replace('\\','/')
MEDIA_URL = '/medias/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static').replace('\\','/'),
)


# 修改上传时文件在内存中可以存放的最大size为10m
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

MYSQL_HOST = '218.244.131.97'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PASS = 'zhiyouba'
MYSQL_DB   = 'bbs'

DATABASES = {
    'default':{
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     MYSQL_DB,
            'USER':     MYSQL_USER,
            'PASSWORD': MYSQL_PASS,
            'HOST':     MYSQL_HOST,
            'PORT':     MYSQL_PORT,
    }
}

# email setting for 123 email server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'zhangxiongcai337@163.com'
EMAIL_HOST_PASSWORD = '3141592653'
EMAIL_USE_SSL = False
