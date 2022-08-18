from django.contrib import admin
from django.urls import include, path

from apps.core.views import ChangeLogView
from apps.movies.views import HomeView

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns
from .urls import urlpatterns as apps_urlpatterns

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("accounts/", include("allauth.urls")),
    path("changelog/", ChangeLogView.as_view(), name="changelog"),
    path("mission-control-center/", admin.site.urls),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    # Custom checks at lib/health_checks
    path("health/", include("health_check.urls")),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
urlpatterns += apps_urlpatterns
