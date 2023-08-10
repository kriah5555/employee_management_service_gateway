from django.http import HttpResponse
from django.http.response import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from .permissions import AccessToken
from .utils import get_microservice_url, headers_to_forward
from .serializers import LoginSerializer
from django.conf import settings

# Create your views here.

class ServiceRequest(APIView):
    permission_classes = [AccessToken]
    renderer_classes   = (JSONRenderer, )

    def api_request(self, request, service_name, path, id=None, action=None):
        service_base_url = get_microservice_url(service_name)
        url = service_base_url + '/' + path
        if id is not None:
            url = url + '/' + id
        if action is not None:
            url = url + '/' + action
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers_to_forward(request.headers.items()),
            data=request.body,
            cookies=request.COOKIES,
            allow_redirects=False,
        )
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers = headers_to_forward(response.headers.items())
        )

    def get(self, request, service_name, path, id=None, action=None):
        return self.api_request(request, service_name, path, id, action)

    def post(self, request, service_name, path, id=None, action=None):
        return self.api_request(request, service_name, path, id, action)

    def put(self, request, service_name, path, id=None, action=None):
        return self.api_request(request, service_name, path, id, action)

    def delete(self, request, service_name, path, id=None, action=None):
        return self.api_request(request, service_name, path, id, action)


class Login(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            service_base_url = get_microservice_url('identity-manager')
            url = service_base_url + '/login'
            payload = {
                "username": serializer.validated_data['username'],
                "password": serializer.validated_data['password'],
            }
            response = requests.post(url, data=payload)
            return HttpResponse(
                content=response.content,
                status=response.status_code,
                headers=headers_to_forward(request.headers.items()),
            )
        else:
            return HttpResponse(serializer.errors, status=400)