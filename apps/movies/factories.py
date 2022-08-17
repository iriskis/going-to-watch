import factory

from . import models


class MovieFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Movie instance."""
    title = factory.Faker("name")
    description = factory.Faker("text")
    poster = factory.django.ImageField(color=factory.Faker("color"))
    kinopoisk_id = factory.Faker("pyint")
    duration = factory.Faker("time")

    class Meta:
        model = models.Movie


class UserMovieFactory(factory.django.DjangoModelFactory):
    """Factory to generate test UserMovie instance."""
    user = factory.SubFactory("apps.users.factories.UserFactory")
    movie = factory.SubFactory("apps.users.factories.UserFactory")
    is_watched = factory.Faker("pybool")

    class Meta:
        model = models.UserMovie

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        """Generate links to users who liked the movie."""
        if not create:
            return

        if extracted:
            for user in extracted:
                self.likes.add(user)    # pylint: disable=no-member
