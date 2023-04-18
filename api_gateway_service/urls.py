from django.urls import path

from . import views
app_name = 'api_gateway_service'

urlpatterns = [
    path('handle_request/', views.handle_request),
    path('get_refresh_token/', views.get_refresh_token),
]
