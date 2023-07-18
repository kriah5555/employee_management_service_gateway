from django.http import HttpResponse
from django.http.response import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from microservices.models import Microservice
from .permissions import AccessToken

# Create your views here.

class ServiceRequest(APIView):
    # permission_classes = [AccessToken]
    renderer_classes   = (JSONRenderer, )

    def dispatch(self, request, service_name, path, id=None):
        service_obj = get_object_or_404(Microservice, name=service_name)
        service_base_url = service_obj.base_url
        url = service_base_url + '/' + path
        if id is not None:
            url = url + '/' + id
        headers_to_forward = ['Content-Type', 'Authorization']
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers.items() if key in headers_to_forward},
            data=request.body,
            cookies=request.COOKIES,
            allow_redirects=False,
        )
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            headers = {key: value for key, value in response.headers.items() if key in headers_to_forward}
        )