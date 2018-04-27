"""
Django settings for aom project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#APPEND_SLASH=False 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5wcm@zoa=ip_6y5)5esig=#kq)-b(_#q%@xsfa%mju&)17u(bi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'pps',
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

ROOT_URLCONF = 'aom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'aom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aom',
        'USER':'root',
        'PASSWORD':'root123',
        'HOST':'localhost',
        'PORT':'3306',
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  #  {
  #      'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  #  },
  #  {
  #      'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  #  },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
  #  {
  #      'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  #  },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


PROJECT_PATH=os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT=os.path.join(os.path.dirname(PROJECT_PATH),'static')
STATIC_URL = '/static/'
STATICFILES_DIRS=(
('css',os.path.join(STATIC_ROOT,'css')),
('fonts',os.path.join(STATIC_ROOT,'fonts')),
('img',os.path.join(STATIC_ROOT,'img')),
('js',os.path.join(STATIC_ROOT,'js')),
('plugins',os.path.join(STATIC_ROOT,'plugins')),
('tools',os.path.join(STATIC_ROOT,'css')),
('bootstrap',os.path.join(STATIC_ROOT,'bootstrap')),
('html',os.path.join(STATIC_ROOT,'html')),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }, # 针对 DEBUG = True 的情况
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(filename)s[%(lineno)d] - %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
             'formatter':'standard'
        },
        'console':{
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers' :['console','mail_admins'],
            'level':'DEBUG',
            'propagate': True # 是否继承父类的log信息
        }, # handlers 来自于上面的 handlers 定义的内容
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}