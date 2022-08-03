import traceback

from rest_framework import permissions, status

from drf_spectacular import drainage, openapi

from . import serializers


class AutoSchema(openapi.AutoSchema):
    """Extend drf_spectacular's AutoSchema.

    Issue in drf-spectacular about 40X responses:
        https://github.com/tfranzel/drf-spectacular/issues/101
    Inspired by:
        https://github.com/tfranzel/drf-spectacular/issues/101#issuecomment-1069383391

    """

    def _get_response_bodies(self, direction="response"):
        """Extend response body with 40X errors bodies.

        Add 401, 403 if endpoint requires authentication or permissions.
        Add 404 if endpoint's url has any params
        Add 400 if it is not safe method and not DELETE method

        """
        response_bodies = super()._get_response_bodies(direction=direction)

        status_codes = set()

        if self.get_auth():
            status_codes.add(status.HTTP_401_UNAUTHORIZED)
            status_codes.add(status.HTTP_403_FORBIDDEN)

        is_not_safe_method = self.method not in permissions.SAFE_METHODS
        is_not_delete = self.method != "DELETE"
        if is_not_safe_method and is_not_delete:
            status_codes.add(status.HTTP_400_BAD_REQUEST)

        is_list_endpoint = self.method == "GET" and self._is_list_view()
        is_endpoint_has_any_params = any(
            filter(lambda _: _["in"] == "path", self._get_parameters()),
        )
        if not is_list_endpoint and is_endpoint_has_any_params:
            status_codes.add(status.HTTP_404_NOT_FOUND)

        error_response_bodies = {
            status.HTTP_401_UNAUTHORIZED: serializers.ErrorDetailSerializer,
            status.HTTP_403_FORBIDDEN: serializers.ErrorDetailSerializer,
            status.HTTP_404_NOT_FOUND: serializers.ErrorDetailSerializer,
        }
        if (
            status.HTTP_400_BAD_REQUEST in status_codes and
            status.HTTP_400_BAD_REQUEST not in response_bodies
        ):
            response_body = self._get_validation_errors_response(
                serializer=self.get_request_serializer(),
            )
            if response_body:
                error_response_bodies[status.HTTP_400_BAD_REQUEST] = (
                    response_body
                )
            else:
                error_response_bodies[status.HTTP_400_BAD_REQUEST] = (
                    serializers.ValidationErrorResponseSerializer
                )
        for code in status_codes:
            if code in response_bodies:
                continue
            response_bodies[code] = self._get_response_for_code(
                serializer=error_response_bodies[code],
                status_code=str(code),
            )
        return response_bodies

    def _get_validation_errors_response(self, serializer):
        """Set up validation error response."""
        if not serializer:
            return None
        try:
            if isinstance(serializer, type):
                serializer = serializer()
            return serializer.error_details_serializer
        except Exception as error:  # pylint: disable=broad-except
            drainage.warn(
                f"Failed to get validation_errors_serializer for "
                f"{serializer.__class__}.\n"
                f"Error: {error}.\n"
                f"{traceback.format_exc()}"
                "Possible solutions:\n"
                "1) Add `ValidationErrorsGeneratorMixin` to it\n"
                "2) Implement property method "
                "`validation_errors_serializer_response`\n"
                "3) Add your own response via `extend_schema_view`.",
            )
        return None
