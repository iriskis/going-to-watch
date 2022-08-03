import copy
import itertools

from django.conf import settings
from django.core.exceptions import ValidationError

from rest_framework import exceptions, request, serializers

from libs.open_api import (
    OpenApiSerializer,
    OpenApiSerializerMixin,
    ValidationErrorsGeneratorMixin,
)


class BaseListSerializer(OpenApiSerializerMixin, serializers.ListSerializer):
    """List Base Serializer with common logic.

    Original `run_validation` returns a dict with `non_field_errors`.
    >>> {'non_field_errors': <raised_error>}

    But since our errors map to the child objects, we replicate
    the behavior when an error occurs in a child serializer:
    >>> {
    ...     "data" : [
    ...         {}, # valid
    ...         {"non_field_errors": ["some error"]},
    ...     ]
    ... }

    If there are errors with whole list in general, we return
    >>> {
    ...     "non_field_errors" : [
    ...         "Error message"
    ...     ]
    ... }

    """

    def __init__(self, *args, **kwargs):
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request = self.context.get("request")
        self._user = getattr(self._request, "user", None)

    def run_validation(self, data=serializers.empty):
        """Override the default `run_validation` to return a list of errors."""
        try:
            (is_empty_value, data) = self.validate_empty_values(data)
            if is_empty_value:
                return data

            value = self.to_internal_value(data)
            self.run_validators(value)
            return self.validate(value)
        except exceptions.ValidationError as error:
            if (
                isinstance(error.detail, list) and
                isinstance(error.detail[0], dict)
            ):
                raise exceptions.ValidationError(
                    dict(data=error.detail),
                )
            raise exceptions.ValidationError(
                {
                    settings.REST_FRAMEWORK.get(
                        "NON_FIELD_ERRORS_KEY",
                        "non_field_errors",
                    ): (
                        error.detail
                        if isinstance(error.detail, list)
                        else [error.detail]
                    ),
                },
            )


class BaseSerializer(ValidationErrorsGeneratorMixin, OpenApiSerializer):
    """Serializer with common logic."""

    def __init__(self, *args, **kwargs):
        """Set current user."""
        super().__init__(*args, **kwargs)
        self._request: request.Request = self.context.get("request")
        self._user = getattr(self._request, "user", None)

    @property
    def _meta(self):
        """Get `Meta` class.

        Used to avoid adding `pylint: disable=no-member`

        """
        # pylint: disable=no-member
        return self.Meta

    @classmethod
    def many_init(cls, *args, **kwargs):
        """Same as original, but we use custom default list serializer."""
        list_kwargs = {
            "allow_empty": kwargs.pop("allow_empty", None),
            "max_length": kwargs.pop("max_length", None),
            "min_length": kwargs.pop("min_length", None),
            "child": cls(*args, **kwargs),
        }
        list_kwargs.update({
            key: value for key, value in kwargs.items()
            if key in serializers.LIST_SERIALIZER_KWARGS
        })
        list_serializer_class = getattr(
            getattr(cls, "Meta", None),
            "list_serializer_class",
            BaseListSerializer,
        )
        return list_serializer_class(*args, **list_kwargs)


class ModelBaseSerializer(BaseSerializer, serializers.ModelSerializer):
    """Model Serializer with common logic."""

    def get_instance(self, attrs: dict):
        """Get instance depending on request."""
        if self.instance:  # if it's update request
            return copy.deepcopy(self.instance)
        # If attrs have `id` data, get instance form db
        # if it is a create request, we return empty instance
        instance_id = attrs.get("id")
        instance = self._meta.model.objects.filter(pk=instance_id).first()
        return instance or self._meta.model()

    def prepare_instance(self, attrs: dict):
        """Prepare instance depending on create/update.

        If `create` used, create empty instance and set fields' values with
        received data.
        If `update` used, update existing instance with received data.

        """
        # Prepare instance depending on create/update
        instance = self.get_instance(attrs)

        # skip creating/updating instance related objects
        relations = self._get_relations_fields_names()

        # Set new data for instance, while ignoring relations
        for attr, value in attrs.items():
            if attr not in relations:
                setattr(instance, attr, value)

        return instance

    def validate(self, attrs: dict) -> dict:
        """Call model's `.clean()` method during validation.

        Create:
            Just create model instance using provided data.
        Update:
            `self.instance` contains instance with new data. We apply passed
            data to it and then call `clean` method for this temp instance.

        """
        attrs = super().validate(attrs)

        instance = self.prepare_instance(attrs)

        try:
            instance.clean()
        except ValidationError as error:
            if not hasattr(error, "error_dict"):
                raise error
            error_dict = {}
            for field, errors in error.error_dict.items():
                errors = list(
                    itertools.chain.from_iterable(
                        field_error.messages for field_error in errors
                    ),
                )
                if not hasattr(
                    self.fields.get(field, None),
                    "error_details_serializer",
                ):
                    error_dict[field] = errors
                    continue
                # If we used serializer for field, we need make error as dict
                # to match spec
                non_field = settings.REST_FRAMEWORK["NON_FIELD_ERRORS_KEY"]
                error_dict[field] = {
                    non_field: errors,
                }
            raise exceptions.ValidationError(error_dict)
        return attrs

    def _get_relations_fields_names(self) -> set[str]:
        """Extract fields with relations before validation."""
        relations = set()

        # Remove related fields from validated data for future manipulations
        for _, field in self.fields.items():
            if field.read_only:
                continue

            if "." in field.source:
                source_attr = field.source.split(".")[0]
                relations.add(source_attr)
                continue

            is_many_model_serializer = (
                isinstance(field, serializers.ListSerializer)
                and isinstance(field.child, serializers.ModelSerializer)
            )
            is_model_serializer = (
                isinstance(field, serializers.ModelSerializer)
            )
            is_m2m_serializer = (
                isinstance(field, serializers.ManyRelatedField)
            )
            if (
                is_many_model_serializer
                or is_model_serializer
                or is_m2m_serializer
            ):
                relations.add(field.source)

        return relations
