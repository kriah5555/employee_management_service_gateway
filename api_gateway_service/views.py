import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib

from .models import Service


def handle_request(request):
    # Get the service name from the URL
    service_name = request.path.split('/')[1]
    
    # Call the API gateway to get the base URL for the service
    api_gateway_url = 'http://localhost:8000/api/gateway/'
    response = requests.get(api_gateway_url + service_name + '/')
    if response.status_code != 200:
        return HttpResponse(status=500)
    service_url = response.json()['service_url']
    
    # Check the API key for authorization
    api_key = request.META.get('HTTP_X_API_KEY')
    if api_key != 'your_api_key':
        return HttpResponse(status=401)
    
    # Forward the request to the microservice
    url = service_url + request.path
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers.items()
                 if key != 'Host'},
        data=request.body,
        cookies=request.COOKIES,
        allow_redirects=False,
    )
    
    # Return the response from the microservice
    return HttpResponse(
        content=response.content,
        status=response.status_code,
        headers={key: value for key, value in response.headers.items()
                 if key != 'Transfer-Encoding'},
    )


def get_refresh_token(request):
    # Get the API key from the request headers
    api_key = request.META.get('HTTP_X_API_KEY')

    # Check if the API key is registered
    try:
        service = Service.objects.get(api_key=api_key)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Invalid API key'})

    # Request a refresh token
    if service.refresh_token_url and service.client_id and service.client_secret:
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': request.POST.get('refresh_token'),
            'client_id': service.client_id,
            'client_secret': service.client_secret,
        }
        response = requests.post(service.refresh_token_url, data=data)
        return JsonResponse(response.json(), status=response.status_code)

    return JsonResponse({'error': 'Refresh tokens not supported for this service'})


@csrf_exempt
class ServiceView:
    def generate_api_key(self, base_url, name):
        # Combine the base URL and name to create a unique string
        string = f"{base_url}/{name}"

        # Generate an MD5 hash of the string
        hashed = hashlib.md5(string.encode()).hexdigest()

        # Use the first 12 characters of the hash as the API key
        api_key = hashed[:12]

        return api_key

    def post(self, request):
        name = request.POST.get('name')
        url = request.POST.get('url')

        # Generate an API key
        api_key = self.generate_api_key(url, name)

        # Save the service to the database
        service = Service(name=name, url=url, api_key=api_key)
        service.save()

        # Return the API key to the user
        response_data = {'api_key': api_key}
        return JsonResponse(response_data)

    def get(self, request):
        # Retrieve all services from the database
        services = Service.objects.all()

        # Serialize the services into a JSON response
        response_data = [{'name': service.name, 'url': service.url, 'api_key': service.api_key} for service in services]
        return JsonResponse(response_data, safe=False)
