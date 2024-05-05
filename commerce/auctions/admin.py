from django.contrib import admin

# Register your models here.
from .models import Auction_listings, Bids, User_Watchlist, Auction_categories, Comments, Bidding_Book, Closed_Auctions


class Auction_listingsAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "current_price", "photo", "category")


admin.site.register(Auction_listings, Auction_listingsAdmin)
admin.site.register(Bids)
admin.site.register(Auction_categories)
admin.site.register(User_Watchlist)
admin.site.register(Comments)
admin.site.register(Bidding_Book)
admin.site.register(Closed_Auctions)