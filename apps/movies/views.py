from django.views.generic import DetailView, TemplateView

from apps.users import models as users_models


class IndexView(TemplateView):
    """Class-based view to display main page."""
    template_name = "movies/index.html"


class WatchlistView(DetailView):
    """Class-based view to display watchlist page."""
    template_name = "movies/watchlist.html"
    model = users_models.User
    context_object_name = "user_with_watchlist"

    # def get_queryset(self):
    #     self.user = get_object_or_404(
    #         users_models.User,
    #         pk=self.kwargs["user_pk"],
    #     )
    #     return models.UserMovie.objects.filter(user=self.user)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["watchlist_own"] = self.user
    #     return context
