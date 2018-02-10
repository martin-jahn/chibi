from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.chibi.models import ApiToken


class TokenAuthentication(authentication.TokenAuthentication):
    model = ApiToken


class AuthorizedAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    api_language = 'en'
