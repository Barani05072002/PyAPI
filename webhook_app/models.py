import uuid
from django.db import models # type: ignore

class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=64, default=uuid.uuid4().hex)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    account = models.ForeignKey(Account, related_name='destinations', on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])
    headers = models.JSONField()

    def __str__(self):
        return self.url
