from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Class-based view to display main page."""
    template_name = "movies/index.html"
