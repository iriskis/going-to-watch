from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesAppConfig(AppConfig):
    """Default configuration for Movies app."""
    name = "apps.movies"
    verbose_name = _("Movies")
