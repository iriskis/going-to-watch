from django.urls import include, path

urlpatterns = [
   path("auth/", include("apps.users.urls")),
   path("movies/", include("apps.movies.urls")),
]
