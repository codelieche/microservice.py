"""
Django settings for message project.

Generated by 'django-admin startproject' using Django 3.0.x.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把apps添加到path路径中，app统一放apps中
sys.path.append(os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kykf0c+d!ar$v#^8(q^4k1$o%od1bwe1q^ajww@n##73%@r7x5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "*.codelieche.com", "localhost", "*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方app
    "rest_framework",
    "corsheaders",  # 跨域访问
    "django_filters",
    # 自己写的app
    "account",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 第三方中间件
    # 跨域访问 cors
    'corsheaders.middleware.CorsMiddleware',

    # 自定义中间件
    # 如果是api访问用户的，就不对csrf校验
    'utils.middlewares.csrf.ApiDisableCsrfMiddleware',
    'utils.middlewares.sso.CheckTicketMiddleware',  # 检查sso ticket参数的中间件

]

ROOT_URLCONF = 'message.urls.main'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'message.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # mysql数据库的配置使用到了os模块获取环境变量
    # 这样不同开发人员设置好自己的环境变量，就可以使用不同的数据库开发了
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MESSAGE_DEVELOP_DB', 'message_develop'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'root'),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', 3306)
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
# 使用是去设置为False，这样数据库保存的数值就是当前时区的时间值，而不会是UTC的时间值
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# 正式环境static文件要收集到STATIC_ROOT中【项目根目录的上一级】
# STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../static"))

# 开发环境使用STTICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# 上传多媒体文件目录
# 上传的文件也放在项目代码根目录的上一级media目录中
# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../media"))

# 注册用户系统使用哪个用户模型
# 不需要加入中间的models
AUTH_USER_MODEL = 'account.UserProfile'
# 登陆地址: 当使用了login_required装饰器未传入login_url参数，默认会在settings中找LOGIN_URL
LOGIN_URL = "/user/login"
SSO_SERVER_URL = "http://127.0.0.1:8000"
SSO_SERVER_LOGIN_URL = "{}/user/login".format(SSO_SERVER_URL)
REDIRECT_FIELD_NAME = "returnUrl"

# 当前系统服务相关的信息
CURRENT_SERVICE_CODE = "message"

# 使用自定义的后台auth认证方法
AUTHENTICATION_BACKENDS = (
    # LDAP登陆配置
    # 'django_python3_ldap.auth.LDAPBackend',
    # 自定义的登陆Backend
    'account.auth.CustomBackend',
)

# LDAP配置，有需要可以查看django ldap相关文档

# 设置session过期时间
SESION_SAVE_EVERY_REQUEST = True
# 设置SESSION COOKIE过期时间 1h
SESSION_COOKIE_AGE = 60 * 60 * 24 * 60
# sessionid的cookie名字
SESSION_COOKIE_NAME = "msgsessionid"

# Django Rest Framework的配置
REST_FRAMEWORK = {
    # 设置分页
    # 'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.LimitOffsetPagination",
    # 'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.PageNumberPagination",
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.SelfPagination',
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
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}
