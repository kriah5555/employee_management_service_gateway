from rest_framework import permissions
from microservices.models import RefreshToken
from datetime import datetime


class AccessToken(permissions.BasePermission):

    def has_permission(self, request, view):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth is None:
            return False
        token = auth.split()[-1]
        if RefreshToken.objects.filter(token=token, expiry__gte = datetime.now()).exists():
            return True
        else:
            return False