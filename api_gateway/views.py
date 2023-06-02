from django.http import HttpResponse
from django.http.response import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from django.shortcuts import get_object_or_404
from microservices.models import ApiKey, RefreshToken, Microservice
from .permissions import AccessToken

class GetRefreshToken(APIView):
    permission_classes = [AllowAny]
    renderer_classes   = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        api_key = request.data.get('api_key', None)
        if api_key is not None:
            api_key_obj = get_object_or_404(ApiKey, key=api_key)
            refresh_token_obj = RefreshToken.objects.create(api_key = api_key_obj)
            response = {"token" : refresh_token_obj.token}
            return Response(response, status=HTTP_200_OK)
        else:
            response = {"details" : 'Api key missing'}
            return Response(response, status=HTTP_403_FORBIDDEN)

class ServiceRequest(APIView):
    permission_classes = [AccessToken]
    renderer_classes   = (JSONRenderer, )

    def get(self, request, service_name, path):
        service_obj = get_object_or_404(Microservice, name=service_name)
        service_base_url = service_obj.base_url
        url = service_base_url + '/' + path
        headers={key: value for key, value in request.headers.items() if key != 'Host'}
        response = requests.request(
            method=request.method,
            url=url,
            # headers=headers,
            data=request.body,
            cookies=request.COOKIES,
            allow_redirects=False,
        )
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            # headers={key: value for key, value in response.headers.items()
            #         if key != 'Transfer-Encoding'},
        )