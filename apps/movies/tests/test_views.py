from django.test import Client
from django.urls import reverse

import pytest

from .. import factories, models, views


@pytest.fixture(scope="module")
def create_movies(django_db_blocker):
    """Generate 10 movies."""
    with django_db_blocker.unblock():
        factories.MovieFactory.create_batch(10)


@pytest.mark.usefixtures("create_movies")
def test_add_movie_view_base_content(auth_client: Client):
    """Check return base content of AddMovieView class."""
    url = reverse("movies:addmovie")
    response = auth_client.get(url)
    assert response.status_code == 200

    result = tuple(response.context["object_list"])
    expected = tuple(models.Movie.objects.recently_added())
    assert result == expected


@pytest.mark.usefixtures("create_movies")
def test_add_movie_view_search_content(auth_client: Client):
    """Check return base content of AddMovieView class."""
    query = "most_unusual_text"
    expected_movie = factories.MovieFactory(title=query)

    url = reverse("movies:addmovie")
    response = auth_client.get(url, {"search_field": query})
    assert response.status_code == 200
    assert expected_movie in response.context["object_list"]


@pytest.mark.usefixtures("create_movies")
def test_add_movie_view_search():
    """Check search function in AddMovieView class."""
    query = "most_unusual_text"

    # Create 2 objects in db with query string in title and description
    ids = (
        factories.MovieFactory(title=query).pk,
        factories.MovieFactory(description=query).pk,
    )

    query_set = views.AddMovieView.search(query)
    assert query_set.filter(pk__in=ids).count()
