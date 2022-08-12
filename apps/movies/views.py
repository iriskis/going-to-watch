from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Class-based view to display main page."""
    template_name = "movies/watchlist.html"


class WatchlistView(TemplateView):
    """Class-based view to display watchlist page."""
    template_name = "movies/watchlist.html"
