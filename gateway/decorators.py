from functools import wraps
from django.http import HttpResponseForbidden

def authenticate_microservice(api_key):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Verify that the request contains a valid access token
            access_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
            if not verify_access_token(access_token):
                return HttpResponseForbidden()
            
            # Verify that the API key matches
            if request.META.get('HTTP_X_API_KEY') != api_key:
                return HttpResponseForbidden()
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


#usage 
# @authenticate_microservice(api_key='abc123')
# def my_microservice_view(request):
    # your code here