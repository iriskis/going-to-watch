from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, response, views

from libs.open_api import ValidationErrorResponseSerializer


def exception_handler(
    exc: Exception,
    context: dict,
) -> response.Response:
    """Handle simple drf exceptions.

    This custom exception handler for django REST framework wraps
    ValidationErrors into field `data` and adds `detail` field with
    message: If error was raised like this ValidationError("Error"), it will
    wrap it in "non_field_errors" dict


        Unfortunately, there are some problems with the data you committed

    """
    error_message = _(
        "Unfortunately, there are some problems with the data you committed",
    )
    non_fields_errors = settings.REST_FRAMEWORK.get(
        "NON_FIELD_ERRORS_KEY",
        "non_field_errors",
    )
    if not isinstance(exc, exceptions.ValidationError):
        return views.exception_handler(exc=exc, context=context)

    if (
        isinstance(exc.detail, list) and
        exc.detail and
        isinstance(exc.detail[0], str)
    ):
        exc.detail = ValidationErrorResponseSerializer({
            "data": {non_fields_errors: exc.detail},
        }).data
    else:
        exc.detail = {
            "data": exc.detail,
            "detail": error_message,
            "code": "validation_error",
        }
    return views.exception_handler(exc=exc, context=context)
