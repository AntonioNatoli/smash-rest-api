from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

class CustomTokenAuthentication(TokenAuthentication):
    model = Token
    keyword = 'Bearer'
