from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from oauthlib.oauth2 import WebApplicationClient

from api_gateway.settings import API_GATEWAY
from .models import Microservice, ApiKey

def create_api_key(request, microservice_name):
    microservice = get_object_or_404(Microservice, name=microservice_name)
    api_key = ApiKey.objects.create(microservice=microservice)
    return JsonResponse({'api_key': api_key.key})

def get_microservice_by_name(request, microservice_name):
    microservice = get_object_or_404(Microservice, name=microservice_name)
    return JsonResponse({'base_url': microservice.base_url})




def get_access_token(request):
    client = WebApplicationClient(API_GATEWAY['OAUTH2_CLIENT_ID'])
    authorization_url, _ = client.prepare_authorization_request(
        API_GATEWAY['OAUTH2_AUTHORIZATION_URL'])
    return redirect(authorization_url)


def handle_oauth2_callback(request):
    client = WebApplicationClient(API_GATEWAY['OAUTH2_CLIENT_ID'])
    token_url = API_GATEWAY['OAUTH2_TOKEN_URL']
    token_url, headers, body = client.prepare_token_request(
        token_url, authorization_response=request.build_absolute_uri())
    headers['Authorization'] = 'Basic ' + b64encode(
        f"{API_GATEWAY['OAUTH2_CLIENT_ID']}:{API_GATEWAY['OAUTH2_CLIENT_SECRET']}".encode()).decode()
    token_response = requests.post(token_url, headers=headers, data=body, auth=(
        API_GATEWAY['OAUTH2_CLIENT_ID'], API_GATEWAY['OAUTH2_CLIENT_SECRET']))
    client.parse_request_body_response(json.dumps(token_response.json()))
    request.session['access_token'] = client.access_token
    request.session['refresh_token'] = client.refresh_token
    request.session['token_expires_at'] = time.time() + client.expires_in
    return redirect('/')
