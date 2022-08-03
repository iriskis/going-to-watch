from rest_framework import serializers


class OpenApiSerializerMixin:
    """Mixin which adds empty create and update methods.

    Made to avoid warnings about unimplemented methods.

    """

    def create(self, validated_data):
        """Made to avoid warnings about unimplemented methods."""

    def update(self, instance, validated_data):
        """Made to avoid warnings about unimplemented methods."""


class OpenApiSerializer(OpenApiSerializerMixin, serializers.Serializer):
    """Serializer that should be used for customizing open_api spec.

    Made to avoid warnings about unimplemented methods.

    """


class ErrorDetailSerializer(OpenApiSerializer):
    """To show in spec responses like this {detail: text}.

    Used to show error message on 401, 403, 404 or other messages from backend.

    """
    detail = serializers.CharField(
        read_only=True,
        default="Message from backend",
        help_text="Message from backend",
    )
    code = serializers.CharField(
        required=False,
        allow_null=True,
        read_only=True,
        default="Code of error",
        help_text="Code of error",
    )
