from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from apps.movies import models as movie_models

from ..core.admin import BaseAdmin
from . import models


class UserMovieInline(admin.TabularInline):
    """InLine for user's movies list model."""
    model = movie_models.UserMovie


@admin.register(models.User)
class UserAdmin(BaseAdmin, DjangoUserAdmin):
    """UI for User model."""
    ordering = ("email",)
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    list_display = (
        "pk",
        "avatar_thumbnail",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "email",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            None, {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"), {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                ),
            },
        ),
        (
            _("Permissions"), {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    inlines = [
        UserMovieInline,
    ]


@admin.register(models.Friendship)
class FriendshipAdmin(BaseAdmin):
    """UI for `Image` model."""
    search_fields = (
        "user",
        "friend",
        "is_accepted",
    )
    list_display = (
        "pk",
        "user",
        "friend",
        "is_accepted",
    )
