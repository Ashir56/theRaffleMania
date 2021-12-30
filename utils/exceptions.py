from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    # Update the structure of the response data.
    if response is not None:
        customized_response = []
    print(response.data.items())
    for key, value in response.data.items():
        message = value
        print(message)
        customized_response.append(message)

    print(customized_response[0][0])
    response_dict = {
        "success": False,
        "message": customized_response[0][0]
    }
    response.data = response_dict
    return response
