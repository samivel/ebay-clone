from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64) 
    description = models.TextField()
    current_bid = models.FloatField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)