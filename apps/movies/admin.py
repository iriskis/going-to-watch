from django.contrib import admin

from apps.core.admin import BaseAdmin

from . import models


@admin.register(models.Movie)
class MovieAdmin(BaseAdmin):
    """UI for `Movie` model."""
    search_fields = (
        "title",
        "duration",
    )
    list_display = (
        "pk",
        "title",
        "description",
        "kinopoisk_url",
        "duration",
    )


@admin.register(models.UserMovie)
class UserMovieAdmin(BaseAdmin):
    """UI for `UserMovie` model."""
    search_fields = (
        "user",
        "movie",
        "is_watched",
    )
    list_display = (
        "pk",
        "user",
        "movie",
        "is_watched",
    )
