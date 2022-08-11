from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Friendship(BaseModel):
    """Friendship model.

    Collect all friendship requests with accepting friendship status.
    """

    user = models.ForeignKey(
        to="users.User",
        verbose_name=_("User who initiated the friendship"),
        on_delete=models.CASCADE,
        related_name="friendship_initiator",
    )
    friend = models.ForeignKey(
        to="users.User",
        verbose_name=_("User who accepting friendship"),
        on_delete=models.CASCADE,
        related_name="friendship_acceptor",
    )
    is_accepted = models.BooleanField(
        verbose_name=_("Accepting status"),
        default=True,
    )

    class Meta:
        verbose_name = _("Friendship")
        verbose_name_plural = _("Friendships")
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique",
                fields=("user", "friend"),
            ),
        ]
