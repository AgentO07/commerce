from django.contrib.auth.models import AbstractUser
from django.db import models



#Remember that each time you change anything in auctions/models.py,
#you’ll need to first run ***"python manage.py makemigrations"*** and then
#***"python manage.py migrate"*** to migrate those changes to your database.


class User(AbstractUser):
    pass



class Bids(models.Model):
    starting_bid_price = models.IntegerField()
    current_bid_price = models.IntegerField()

class Auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    current_price = models.IntegerField()
    photo = models.URLField(max_length=256)

class Auction_categories(models.Model):
    name = models.CharField(max_length=64) 
    listings = models.ManyToManyField(Auction_listings, related_name='categories')

class Comments():
    pass

class Watchlist(models.Model):
    pass