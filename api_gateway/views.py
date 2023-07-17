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
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin:index')
    return redirect('admin:login')

class GetRefreshToken(APIView):
    permission_classes = [AllowAny]
    renderer_classes   = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        api_key = request.data.get('api_key', None)
        if api_key is not None:
            api_key_obj = get_object_or_404(ApiKey, key=api_key)
            RefreshToken.objects.filter(api_key = api_key_obj, status = True).update(status = False)
            refresh_token_obj = RefreshToken.objects.create(api_key = api_key_obj)
            response = {"token" : refresh_token_obj.token}
            return Response(response, status=HTTP_200_OK)
        else:
            response = {"details" : 'Api key missing'}
            return Response(response, status=HTTP_403_FORBIDDEN)