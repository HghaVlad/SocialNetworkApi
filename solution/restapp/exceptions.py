from rest_framework.exceptions import APIException
from rest_framework import status


class UniqueError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = {"reason": "This value is used"}
