from rest_framework.permissions import BasePermission
from rest_framework import status
import requests
from .utils import get_microservice_url, headers_to_forward
from rest_framework.exceptions import APIException

class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {
        'success': False,
        'message': 'Forbidden'
    }

class AccessToken(BasePermission):


    def has_permission(self, request, view):
        access_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        if access_token:
            service_base_url = get_microservice_url('identity-manager')
            url = service_base_url + '/validate-token'
            response = requests.get(
                url,
                headers=headers_to_forward(request.headers.items()),
            )

            if response.status_code == 200:
                return True
        raise PermissionDenied()