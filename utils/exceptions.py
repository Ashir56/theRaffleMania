from rest_framework.exceptions import ValidationError, AuthenticationFailed, \
    NotAuthenticated, NotFound
from rest_framework.views import exception_handler


def _get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_codes(value) for key, value in detail.items()}
    return detail.code


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    # Update the structure of the response data.
    customized_response = []

    if isinstance(exc, ValidationError):

        if response is not None:
            response.status_code = 500
        codes = _get_codes(response.data)
        code = ''
        for key, value in codes.items():
            code = str(value)

        if 'does_not_exist' in code:
            response_dict = {
                "success": False,
                "message": "Object Does Not Exist"
            }
            response.data = response_dict
        else:
            for key, value in response.data.items():
                message = value
                customized_response.append(message)
            response_dict = {
                "success": False,
                "message": customized_response[0][0]
            }
            response.data = response_dict

    if isinstance(exc, AuthenticationFailed):

        response_dict = {}
        if response is not None:
            response.status_code = 401
            response_dict = {
                "success": False,
                "message": "Authentication Failed"
            }
        response.data = response_dict
    if isinstance(exc, NotAuthenticated):
        response_dict = {}
        if response is not None:
            response.status_code = 401
            response_dict = {
                "success": False,
                "message": "Authentication Credentials were not Provided"
            }
        response.data = response_dict

    if isinstance(exc, NotFound):
        response_dict = {}
        if response is not None:
            response.status_code = 404
            response_dict = {
                "success": False,
                "message": "Object Does Not Exist"
            }
        response.data = response_dict

    return response
