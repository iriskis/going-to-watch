from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from apps.movies.models import Movie, UserMovie
from apps.users.models import User


class WatchlistView(LoginRequiredMixin, DetailView):
    """Display user watchlist page by user uid."""
    template_name = "movies/watchlist.html"
    model = User
    context_object_name = "watchlist_owner"
    slug_field = "uid"

    def get_queryset(self):
        """Add prefetch movies with likes."""
        movie_queryset = UserMovie.objects.with_likes_count()
        return super().get_queryset().prefetch_related(
            models.Prefetch("movies", queryset=movie_queryset),
        )

    def get_context_data(self, **kwargs):
        """Add watchlict to context."""
        context = super().get_context_data(**kwargs)
        context["watchlist"] = self.get_object().movies.unwatched()
        return context


class AddLikeView(View):
    """Add or delete like to user movie."""
    def post(self, request, movie_pk, watchlist_owner_uid):
        """Check user like on movie from other user watchlist."""
        user = request.user
        user_movie = get_object_or_404(UserMovie, pk=movie_pk)
        if user_movie.likes.filter(pk=user.pk).exists():
            user_movie.likes.remove(user)
        else:
            user_movie.likes.add(user)

        return redirect("movies:watchlist", watchlist_owner_uid)


class HomeView(TemplateView):
    """Display main page.

    Use watchlist for homepage if user is authenticated.
    """
    template_name = "movies/index.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect("movies:watchlist", slug=user.uid)
        return super().get(request, *args, **kwargs)


class AddMovieView(LoginRequiredMixin, ListView):
    """Class-based ListView to display add movie page."""
    model = Movie
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

        return Movie.objects.recently_added()

    @staticmethod
    def search(query: str) -> QuerySet:
        """Find movies containing query text in the title or description."""
        query = query.strip()
        search_results = Movie.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
        )
        return search_results


class MovieDetailView(LoginRequiredMixin, DetailView):
    """Class-based DetailView to display movie details page."""
    model = Movie
    context_object_name = "movie"
    template_name = "movies/movie.html"
