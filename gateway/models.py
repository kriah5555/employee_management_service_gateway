from django.db import models

class Microservice(models.Model):
    name = models.CharField(max_length=255)
    base_url = models.URLField()

    def __str__(self):
        return self.name

class ApiKey(models.Model):
    key = models.CharField(max_length=255)
    microservice = models.ForeignKey(Microservice, on_delete=models.CASCADE)

    def __str__(self):
        return self.key
