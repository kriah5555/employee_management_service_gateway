from django.contrib import admin
from .models import Client, ApiKey, RefreshToken, Microservice, RequestLogs

# Register your models here.

admin.site.register(Microservice)
admin.site.register(Client)
admin.site.register(ApiKey)
admin.site.register(RefreshToken)
admin.site.register(RequestLogs)
