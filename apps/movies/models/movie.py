from django.db import models
from django.utils.translation import gettext_lazy as _

from config.settings.common import KINOPOISK_BASE_URL

from apps.core.models import BaseModel

from ..querysets import MovieQuerySet


class Movie(BaseModel):
    """Movie model.

    Save of main characteristics of movie.
    """

    title = models.CharField(
        verbose_name=_("Movie title"),
        max_length=255,
        null=True,
    )
    description = models.TextField(
        verbose_name=_("Movie description"),
        blank=True,
        null=True,
    )
    poster = models.ImageField(
        verbose_name=_("Link to get poster"),
        # images will be uploaded to MEDIA_ROOT / posters
        upload_to="posters/",
        blank=True,
        null=True,
    )
    kinopoisk_id = models.PositiveIntegerField(
        verbose_name=_("Movie ID on kinopoisk"),
        unique=True,
    )
    duration = models.DurationField(
        verbose_name=_("Movie length"),
        help_text=_("Input in minutes or use format DD:hh:mm"),
        null=True,
    )

    objects = MovieQuerySet.as_manager()

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title

    @property
    def kinopoisk_url(self) -> str:
        """Generate link to movie in kinopoisk."""
        return KINOPOISK_BASE_URL + str(self.kinopoisk_id)
