from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

class UserNotExist(APIException):
    default_code = 'user_not_exist'
    default_detail = 'Il tuo account non esiste'
    status_code = HTTP_404_NOT_FOUND


class PasswordWrong(APIException):
    default_code = 'password_wrong'
    default_detail = 'Password errata'
    status_code = HTTP_400_BAD_REQUEST
