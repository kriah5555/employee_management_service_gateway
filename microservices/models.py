from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
from datetime import timedelta, datetime
from users.models import User
from api_gateway.constants import CLIENT_TYPE_CHOICES, REFRESH_TOKEN_LIFESPAN

# Create your models here.

class Microservice(models.Model):
    name = models.CharField(max_length=255)
    base_url = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255, blank=True)
    microservices_access = models.ManyToManyField('Microservice', blank=True, verbose_name = 'Microservices access')
    client_type = models.SmallIntegerField(choices = CLIENT_TYPE_CHOICES, null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'client'
        ordering = ['-id']

class ApiKey(models.Model):
    key = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # microservice = models.ForeignKey(Microservice, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}:{1}".format(self.client, self.key)
    class Meta:
        db_table = 'api_key'
        ordering = ['-id']

@receiver(post_save, sender=Client)
def create_client_api_key(sender, instance=None, created=False, **kwargs):
    if created:
        string = f"{instance.name}"
        hashed = hashlib.md5(string.encode()).hexdigest()
        api_key = hashed[:50]
        ApiKey.objects.create(client=instance, key=api_key)



class RefreshToken(models.Model):
    token = models.CharField(max_length=255)
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.expiry = datetime.now() + timedelta(seconds=REFRESH_TOKEN_LIFESPAN)
        string = f"{self.api_key.key}{datetime.now()}"
        hashed = hashlib.md5(string.encode()).hexdigest()
        self.token = hashed[:50]
        super(RefreshToken, self).save(*args, **kwargs)
    
    def __str__(self):
        return "{0}:{1}".format(self.api_key.client.name, self.token)

    class Meta:
        db_table = 'refresh_token'
        ordering = ['-id']

class RequestLogs(models.Model):
    endpoint = models.CharField(max_length=100, blank=True) # The url the user requested
    response_code = models.PositiveSmallIntegerField() # Response status code
    method = models.CharField(max_length=10, blank=True)  # Request method
    remote_address = models.CharField(max_length=20, blank=True) # IP address of user
    exec_time = models.IntegerField(null=True) # Time taken to create the response
    date = models.DateTimeField(auto_now=True) # Date and time of request
    body_response = models.TextField() # Response data
    body_request = models.TextField() # Request data

    def __str__(self):
        return "{0}:{1} {2}".format(self.remote_address, self.endpoint, self.response_code)

    class Meta:
        db_table = 'request_logs'
        ordering = ['-id']

# class UrlRouting(models.Model):
#     name = models.CharField(max_length=255)
#     microservice = models.ForeignKey(Microservice, on_delete=models.CASCADE)
#     base_url = models.CharField(max_length=255)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name