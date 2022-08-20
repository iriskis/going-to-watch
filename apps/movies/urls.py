from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path(
        "watchlist/<slug:slug>/",
        views.WatchlistView.as_view(),
        name="watchlist",
    ),
    path(
        "movies/add_like/<int:movie_pk>/<int:watchlist_uid>",
        views.AddLikeView.as_view(),
        name="add-like",
    ),
    path("movies/add/", views.AddMovieView.as_view(), name="addmovie"),
    path("movies/<int:pk>/", views.MovieDetailView.as_view(), name="movie"),
]
