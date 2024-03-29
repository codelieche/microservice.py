"""
Django settings for usercenter project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# 把apps添加到path路径中，app统一放apps中
sys.path.append(os.path.join(BASE_DIR, "apps"))
# codelieche的库放在上级目录中, 正式发布的时候需要安装codelieche这个库
# sys.path.append(os.path.join(BASE_DIR, "../../codelieche/src"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%=el5yipkz0n)+2hk8i49ts$b*ijd%7n4b0k_o_z86#fwds91l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方app
    'rest_framework',
    'corsheaders',
    'django_filters',

    # 自己写的app
    'codelieche.django.modellog',
    'account.apps.AccountConfig',
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 第三方中间件：cors
    'corsheaders.middleware.CorsMiddleware',
    # 自定义中间件
    'codelieche.django.middlewares.csrf.ApiDisableCsrfMiddleware',
    'account.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'usercenter.urls.main'

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

WSGI_APPLICATION = 'usercenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # mysql数据库的配置使用到了os模块获取环境变量
    # 这样不同开发人员设置好自己的环境变量，就可以使用不同的数据库开发了
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('USERCENTER_DEVELOP_DB', 'usercenter_001'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'root'),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', 3306)
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 注册用户系统使用哪个用户模型
# 不需要加入中间的models
# AUTH_USER_MODEL = 'account.UserProfile'

# 登陆地址: 当使用了login_required装饰器未传入login_url参数，默认会在settings中找LOGIN_URL
# LOGIN_URL = "/user/login"

# 使用自定义的后台auth认证方法
# AUTHENTICATION_BACKENDS = (
#     # LDAP登陆配置
#     # 'django_python3_ldap.auth.LDAPBackend',
#     # 自定义的登陆Backend
#     'account.auth.CustomBackend',
# )

# 设置session过期时间
SESION_SAVE_EVERY_REQUEST = True
# 设置SESSION COOKIE过期时间 1d
SESSION_COOKIE_AGE = 60 * 60 * 24

# Django Rest Framework的配置
REST_FRAMEWORK = {
    # 设置分页
    # 'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.LimitOffsetPagination",
    # 'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.PageNumberPagination",
    'DEFAULT_PAGINATION_CLASS': 'codelieche.django.pagination.SelfPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 为了调试，需要BrowsableAPIRenderer,生产环境需要注释下面这行
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 设置DatetimeField字段的格式
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    # 用户认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'account.auth.JwtAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'UNAUTHENTICATED_USER': 'account.models.user.AnonymousUser',
}

# 跨域访问相关配置
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'OPTIONS',
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-headers',
    'x-team-id'
]

APPEND_SLASH = False

# 加密的密码
PASSWORD_KEY = os.environ.get("PASSWORD_KEY", "0000000000000000")
# JWT Secret值
JWT_SECRET = os.environ.get("JWT_SECRET", "codelieche")

# Redis相关
REDIS_HOST_PORT = os.environ.get("REDIS_HOST_PORT", '127.0.0.1:6379')
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", '')
REDIS_CACHE_DB = os.environ.get("REDIS_CACHE_DB", '10')

# 缓存配置
# 缓存key的前缀，默认是空
CACHE_KEY_PREFIX = os.environ.get("CACHE_KEY_PREFIX", "usercenter")
CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT", '300')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://:{}@{}'.format(REDIS_PASSWORD, REDIS_HOST_PORT),
        'KEY_PREFIX': CACHE_KEY_PREFIX,
        'TIMEOUT': int(CACHE_DEFAULT_TIMEOUT),
        'OPTIONS': {
            'db': REDIS_CACHE_DB,
            'parser_class': 'redis.connection.PythonParser',
            'pool_class': 'redis.BlockingConnectionPool',
        }
    }
}
