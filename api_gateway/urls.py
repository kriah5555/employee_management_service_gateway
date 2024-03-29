"""
URL configuration for api_gateway project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from . import views as ApiGatewayViews
from microservices import views as MicroserviceViews

urlpatterns = [
    path("", ApiGatewayViews.home, name="home"),
    path("admin/", admin.site.urls),
    path(
        "get-refresh-token",
        ApiGatewayViews.GetRefreshToken.as_view(),
        name="get-refresh-token",
    ),
    path(
        "service/<str:service_name>/<str:path>",
        MicroserviceViews.ServiceRequest.as_view(),
    ),
    path(
        "service/<str:service_name>/<str:path>/<str:id>",
        MicroserviceViews.ServiceRequest.as_view(),
    ),
    path(
        "service/<str:service_name>/<str:path>/<str:id>/<str:action>",
        MicroserviceViews.ServiceRequest.as_view(),
    ),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    # path("service/login", MicroserviceViews.Login.as_view()),
]
