from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path(
        "watchlist/<int:pk>/",
        views.WatchlistView.as_view(),
        name="watchlist",
    ),
]
