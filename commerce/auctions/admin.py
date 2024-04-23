from django.contrib import admin

# Register your models here.
from .models import Auction_listings, Bids, Auction_categories

admin.site.register(Auction_listings)
admin.site.register(Bids)
admin.site.register(Auction_categories)
    