"""
Django settings for storyworlds project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import environ

###############################################################################
# Environment configuration
###############################################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=[])
DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
defaultdb = "spatialite:///%s/db.sqlite3" % BASE_DIR
DATABASES = {"default": env.db(default=defaultdb)}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = "/static/"


###############################################################################
# Tunable Parameters
###############################################################################
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-US"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_L10N = True
USE_TZ = True

TAGGIT_CASE_INSENSITIVE = True


###############################################################################
# Project Composition
###############################################################################
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    # {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    # {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "adminsortable2",
    "taggit",
    "worlds",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# In DEV environments, install dev apps and middlewares too.
if DEBUG:
    try:
        import debug_toolbar

        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    except ImportError:
        # Not an error if we don't have it.
        pass

    try:
        import django_extensions

        INSTALLED_APPS += ["django_extensions"]
    except ImportError:
        # Not an error if we don't have it.
        pass

ROOT_URLCONF = "storyworlds.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "storyworlds.wsgi.application"
