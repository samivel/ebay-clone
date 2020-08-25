from django.contrib.auth.models import AbstractUser
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=64) 
    description = models.TextField()
    current_bid = models.FloatField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, null=True)
    seller = models.IntegerField()
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f'Listing: {self.title}'



class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name='watchers')


class Bid(models.Model):
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='current_bidder')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='current_bidder')