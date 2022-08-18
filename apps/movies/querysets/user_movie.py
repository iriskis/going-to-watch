from django.db import models


class UserMovieQuerySet(models.QuerySet):
    """Custom QuerySet for UserMovie model."""
    def watched(self):
        """Return queryset of watched users movies."""
        return self.filter(is_watched=True)

    def unwatched(self):
        """Return queryset of not watched users movies."""
        return self.filter(is_watched=False)

    def with_likes_count(self):
        """Return queryset with annotated likes count."""
        return self.annotate(
            likes_count=models.Count("likes"),
        )
