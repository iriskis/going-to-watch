from django.core.management.base import BaseCommand

from ...factories import MovieFactory


class Command(BaseCommand):
    """CLI for generate test movie objects in db."""
    help = """Script to generate test movie objects in db"""

    def add_arguments(self, parser):
        """Accepts arguments."""
        parser.add_argument(
            "count",
            nargs="?",
            type=int,
            default=1,
            help="Count of movies to generate",
        )

    def handle(self, *args, **options):
        """Generates movies in db in the amount of 'count' pieces."""
        count = options.get("count")
        MovieFactory.create_batch(count)
