from django.contrib import admin

from apps.core.admin import BaseAdmin

from . import models


@admin.register(models.Movie)
class MovieAdmin(BaseAdmin):
    """UI for `Movie` model."""
    search_fields = (
        "title",
        "description",
    )
    list_display = (
        "pk",
        "title",
        "description",
        "kinopoisk_id",
        "duration",
    )
    list_display_links = (
        "pk",
        "title",
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
    list_display_links = (
        "pk",
        "user",
        "movie",
    )
