from django.contrib.auth.models import AbstractUser
from django.db import models



#Remember that each time you change anything in auctions/models.py,
#you’ll need to first run ***"python manage.py makemigrations"*** and then
#***"python manage.py migrate"*** to migrate those changes to your database.


class User(AbstractUser):
    pass

class Auction_listings():
    pass

class Bids():
    pass

class Comments():
    pass

