from microservices.models import Microservice
from django.shortcuts import get_object_or_404

def get_microservice_url(service_name):
    service_obj = get_object_or_404(Microservice, name=service_name)
    return service_obj.base_url

def headers_to_forward(headers):
    headers_to_forward = ['Content-Type', 'Authorization']
    return {key: value for key, value in headers if key in headers_to_forward}