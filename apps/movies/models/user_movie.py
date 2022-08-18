from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.movies.querysets import UserMovieQuerySet


class UserMovie(BaseModel):
    """User movie which user going to watch.

    Mark a movie as watched.
    Сollect likes on movie from friends.
    """

    user = models.ForeignKey(
        to="users.User",
        related_name="movies",
        verbose_name=_("User who add movie"),
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        to="movies.Movie",
        related_name="users",
        verbose_name=_("Added movie"),
        on_delete=models.CASCADE,
    )
    is_watched = models.BooleanField(
        verbose_name=_("Movie watching status"),
        default=False,
    )
    likes = models.ManyToManyField(
        to="users.User",
        verbose_name=_("Likes by friends"),
        related_name=_("likes"),
        blank=True,
    )
    objects = UserMovieQuerySet.as_manager()

    class Meta:
        verbose_name = _("UserMovie")
        verbose_name_plural = _("UsersMovies")
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique",
                fields=("user", "movie"),
            ),
        ]

    def __str__(self):
        return self.movie.title
