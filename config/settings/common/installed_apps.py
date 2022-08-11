from .health_check import HEALTH_CHECKS_APPS

# Application definition
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
)

DRF_PACKAGES = (
    "rest_framework",
    "django_filters",
    "knox",
    "drf_spectacular",
)

THIRD_PARTY = (
    "corsheaders",
    "storages",
    "imagekit",
    "django_celery_beat",
    "django_extensions",

    # django-allauth apps for Google OAuth 2.0
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
)

LOCAL_APPS = (
    "apps.core",
    "apps.users",
    "apps.movies",
)

INSTALLED_APPS += DRF_PACKAGES + THIRD_PARTY + HEALTH_CHECKS_APPS + LOCAL_APPS
