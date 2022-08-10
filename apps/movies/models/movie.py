from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Movie(BaseModel):
    """Movie model.

    Save of main characteristics of movie.
    """

    title = models.CharField(
        verbose_name=_("Movie title"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("Movie description"),
        blank=True,
    )
    poster = models.ImageField(
        verbose_name=_("Link to get poster"),
        # images will be uploaded to MEDIA_ROOT / posters
        upload_to="posters/",
        blank=True,
    )
    kinopoisk_url = models.URLField(
        verbose_name=_("Link to kinopoisk page"),
        max_length=255,
    )
    duration = models.DurationField(
        verbose_name=_("Movie length"),
        help_text=_("Input in minutes or use format DD:hh:mm"),
    )

    class Meta:
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")

    def __str__(self):
        return self.title
