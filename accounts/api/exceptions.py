from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from django.utils.encoding import force_text


# class EmptyFieldException(APIException):
#     status_code = 200
#     default_detail = "You need to enter both email and password to log in."
#     default_code = "cannot log in"


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None: self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else:
            self.detail = {'detail': force_text(self.default_detail)}


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = status.HTTP_200_OK

    return response
