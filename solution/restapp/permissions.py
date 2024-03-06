from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken


class IsTokenAvailable(BasePermission):
    message = {'reason': "The token was made before updating password. Please sign-in again."}

    def has_permission(self, request, view):
        token = decode(str(request.auth), settings.SECRET_KEY, algorithms="HS256")
        if token['password_hash'] != request.user.password:
            raise AuthenticationFailed(detail=self.message)
        return True


class MyToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["password_hash"] = user.password

        return token
