from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=50)
    base_url = models.URLField()
    api_key = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=255, null=True)
    refresh_token_expiration = models.DateTimeField(null=True)
    client_id = models.CharField(max_length=100, blank=True, null=True)
    client_secret = models.CharField(max_length=100, blank=True, null=True)
    
    def generate_api_key(self):
        # generate API key using base_url and name
        api_key = f"{self.base_url}/{self.name}".encode("utf-8")
        api_key = hashlib.sha256(api_key).hexdigest()[:50]
        self.api_key = api_key
    
    def generate_refresh_token(self):
        # generate refresh token
        refresh_token = str(uuid.uuid4())
        self.refresh_token = refresh_token
        self.refresh_token_expiration = timezone.now() + timedelta(seconds=30)
