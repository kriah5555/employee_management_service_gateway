from django.urls import path

from . import views
app_name = 'gateway'

urlpatterns = [
    path('api_key/<str:microservice_name>/', views.create_api_key, name='create_api_key'),
    path('microservice/<str:microservice_name>/', views.get_microservice_by_name, name='get_microservice_by_name'),
]
