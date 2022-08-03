from django.conf import settings
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .open_api import (
    ErrorDetailSerializer,
    OpenApiSerializer,
    OpenApiSerializerMixin,
)


class ValidationErrorsField(
    OpenApiSerializerMixin,
    serializers.ListSerializer,
):
    """Field that shows validation errors.

    Used to represent list of errors for single field, like this:
        {
            "data": {
                "field_name": [  <--- this field
                    "Value should be greater 100",
                    "Value should be less 200"
                ]
            }
        }

    """

    def __init__(self, field_name: str):
        super().__init__(
            required=False,
            allow_null=True,
            allow_empty=False,
            child=serializers.CharField(
                default="Field validation error",
                help_text="Field validation error",
            ),
            help_text="List of errors for field",
        )
        self.field_name = field_name


class ValidationErrorSerializer(OpenApiSerializer):
    """Validation error which came directly instead of serializer."""

    @cached_property
    def fields(self):
        """Add field for non fields errors."""
        fields = super().fields
        non_field_errors = settings.REST_FRAMEWORK["NON_FIELD_ERRORS_KEY"]
        fields[non_field_errors] = ValidationErrorsField(
            field_name=non_field_errors,
        )
        return fields


class ValidationErrorResponseSerializer(ErrorDetailSerializer):
    """Validation error response."""
    data = ValidationErrorSerializer()
    detail = serializers.CharField(
        default=_(
            "Unfortunately, there are some problems with"
            " the data you committed",
        ),
        help_text="Error message",
    )

    @cached_property
    def fields(self):
        """Add default for code."""
        fields = super().fields
        fields["code"].default = "validation_error"
        return fields


# Need this, because every time `validation_errors_serializer` is called a
# completely new class is generated, which confuses drf-spectacular.
__VALIDATION_SERIALIZERS_MAP__ = {}
__VALIDATION_LIST_SERIALIZERS_MAP__ = {}
__VALIDATION_SERIALIZERS_RESPONSE_MAP__ = {}


class ValidationErrorsGeneratorMixin:
    """Mixin which generates errors serializer for open api spec."""

    @property
    def validation_errors_serializer(self):
        """Generate validation errors serializer."""
        if self.__class__ in __VALIDATION_SERIALIZERS_MAP__:
            return __VALIDATION_SERIALIZERS_MAP__[self.__class__]
        fields = self._get_validation_errors_serializer_fields()

        class _ValidationErrorsSerializer(OpenApiSerializer):
            """Serializer to show validation errors."""

            def __init__(
                self,
                field_name: str = None,
                required: bool = True,
                *args,
                **kwargs,
            ):
                super().__init__(
                    required=required,
                    *args,
                    **kwargs,
                )
                self.field_name = field_name

            @cached_property
            def fields(self) -> dict:
                """Set up fields.

                Return generated error fields from serializer.

                """
                return fields

        class_name = (
            f"{self.__class__.__name__.replace('Serializer', '')}"
            f"ValidationErrorsSerializer"
        )
        __VALIDATION_SERIALIZERS_MAP__[self.__class__] = type(
            class_name,
            (_ValidationErrorsSerializer,),
            {},
        )
        return __VALIDATION_SERIALIZERS_MAP__[self.__class__]

    @property
    def error_details_serializer(self):
        """Generate validation errors serializer response."""
        if self.__class__ in __VALIDATION_SERIALIZERS_RESPONSE_MAP__:
            return __VALIDATION_SERIALIZERS_RESPONSE_MAP__[self.__class__]

        class _ValidationErrorSerializer(ValidationErrorResponseSerializer):
            """Validation error response."""
            data = self.validation_errors_serializer()

        class_name = (
            f"{self.__class__.__name__.replace('Serializer', '')}"
            f"ValidationErrorResponseSerializer"
        )
        __VALIDATION_SERIALIZERS_RESPONSE_MAP__[self.__class__] = type(
            class_name,
            (_ValidationErrorSerializer,),
            {},
        )
        return __VALIDATION_SERIALIZERS_RESPONSE_MAP__[self.__class__]

    def _get_fields_validation_errors_serializer(self) -> dict:
        """Get a dict of fields for validation errors serializer."""
        return {
            field_name: field
            for field_name, field in self.get_fields().items()
            if not field.read_only
        }

    def _get_validation_errors_serializer_fields(self) -> dict:
        """Get mapping of fields that can generate validation error."""
        serializer_fields = self._get_fields_validation_errors_serializer()
        fields = {
            field_name: self._generate_validation_error_field(
                field_name=field_name,
                field=field,
            )
            for field_name, field in serializer_fields.items()
        }
        non_field_label = settings.REST_FRAMEWORK["NON_FIELD_ERRORS_KEY"]
        fields[non_field_label] = ValidationErrorsField(
            field_name=non_field_label,
        )
        return fields

    def _generate_validation_error_field(
        self,
        field_name: str,
        field: serializers.Field,
    ):
        """Generate serializer field error for field."""
        if hasattr(field, "validation_errors_serializer"):
            return field.validation_errors_serializer(
                field_name=field_name,
                required=False,
            )
        if isinstance(field, serializers.ListSerializer):
            return self._generate_validation_errors_field(
                name=field_name,
                field=field.child,
            )(
                field_name=field_name,
                required=False,
            )
        return ValidationErrorsField(field_name=field_name)

    def _generate_validation_errors_field(
        self,
        field,
        name,
    ):
        """Generate validation errors serializer for list.

        Same as _generate_validation_error_field, but we need to wrap it in
        list serializer.

        """
        if self.__class__ in __VALIDATION_LIST_SERIALIZERS_MAP__:
            return __VALIDATION_LIST_SERIALIZERS_MAP__[self.__class__]
        fields = {}
        errors = serializers.ListSerializer(
            required=False,
            allow_null=True,
            allow_empty=False,
            child=field.validation_errors_serializer(
                field_name=name,
                required=False,
            ),
            help_text="List of errors for objects",
        )
        errors.field_name = "data"
        fields["data"] = errors
        non_field_label = settings.REST_FRAMEWORK["NON_FIELD_ERRORS_KEY"]
        fields[non_field_label] = ValidationErrorsField(
            field_name=non_field_label,
        )

        class _ValidationErrorsListFieldSerializer(OpenApiSerializer):
            """Serializer to show validation errors in list."""

            def __init__(
                self,
                field_name: str = None,
                required: bool = True,
                *args,
                **kwargs,
            ):
                super().__init__(
                    required=required,
                    *args,
                    **kwargs,
                )
                self.field_name = field_name

            @cached_property
            def fields(self) -> dict:
                """Set up fields."""
                return fields

        class_name = (
            f"{self.__class__.__name__.replace('Serializer', '')}"
            f"ValidationErrorsListFieldSerializer"
        )
        __VALIDATION_LIST_SERIALIZERS_MAP__[self.__class__] = type(
            class_name,
            (_ValidationErrorsListFieldSerializer,),
            {},
        )
        return __VALIDATION_LIST_SERIALIZERS_MAP__[self.__class__]
