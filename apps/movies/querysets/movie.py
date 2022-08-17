from django.db import models


class MovieQuerySet(models.query.QuerySet):
    """Custom QuerySet to add additional methods to movie's QuerySet."""

    def recently_added(self, count: int = 10, *args):
        """Returns movies recently added by users.

        By default, 10 pieces are returned if that many movies are contained
        in the database. If there are less than 'count' movies in the database,
        then as many as there are will be returned.

        Args:
            count: The number of movies to return.

        """
        args = ("-users__created",) + args
        return self.order_by(*args)[:count]
