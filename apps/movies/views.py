from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView

from . import models


class IndexView(TemplateView):
    """Class-based view to display main page."""
    template_name = "movies/index.html"


class AddMovieView(LoginRequiredMixin, ListView):
    """Class-based ListView to display add movie page."""
    model = models.Movie
    template_name = "movies/add_movie.html"
    context_object_name = "movies"
    extra_context = {"query": ""}
    paginate_by = 10

    def get_queryset(self):
        """Load movies for add movie page."""
        query = self.request.GET.get("search_field")
        self.extra_context["query"] = query

        if query:
            return self.search(query)

        return models.Movie.objects.recently_added()

    @staticmethod
    def search(query: str) -> QuerySet:
        """Find movies containing query text in the title or description."""
        query = query.strip()
        search_results = models.Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
        )
        return search_results


class MovieDetailView(LoginRequiredMixin, DetailView):
    """Class-based DetailView to display movie details page."""
    model = models.Movie
    context_object_name = "movie"
    template_name = "movies/movie.html"
