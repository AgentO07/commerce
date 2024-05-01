from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Auction_listings, Bids, Auction_categories, User_Watchlist, Comments
from django.contrib.auth.decorators import login_required
    


#Adding the @login_required decorator on top of any view will ensure that only a user who is logged in can access that view.


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# login req
@login_required
def create_new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid_price = request.POST["starting_bid_price"]
        url = request.POST["url"]
        category = request.POST["category"]

        Auction_listings.objects.create(
            title = title,
            description = description,
            photo = url,
            current_price = starting_bid_price,
            category = category
        )

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_new_listing.html", {
        "category_list": Auction_categories.objects.all()
    })

def active_listing(request):

    return render(request, "auctions/active_listing.html", {
        "Act_listings": Auction_listings.objects.all()
    })


def Users(request):
    return render(request, "auctions/Users.html", {
        "Users": User.objects.all()
    })


def listing(request, req_list):
    x_listing = Auction_listings.objects.get(title=str(req_list))
    comments = x_listing.comment.all()
    if request.user.is_authenticated:
        current_user = request.user
        try:
            current_user_watchlist = User_Watchlist.objects.get(user=current_user)
        except User_Watchlist.DoesNotExist:
            current_user_watchlist =User_Watchlist.objects.create(user=current_user)
        
        if User_Watchlist.objects.filter(user=current_user, listing=x_listing).exists():
            is_in_watchlist = True
            if request.method == "POST":
                current_user_watchlist.listing.remove(x_listing)
            return render(request, "auctions/listing.html", {
                "Listing": x_listing,
                "Comments": comments,
                "is_in_watchlist": is_in_watchlist
            })
        else:
            if request.method == "POST":   
                current_user_watchlist.listing.add(x_listing)
                return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/listing.html", {
        "Listing": x_listing,
        "Comments": comments
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "Categories": Auction_categories.objects.all()
    })


def category(request, called_category):
    category_x = Auction_categories.objects.get(name=str(called_category))
    Listings_x = category_x.listings.all()
    return render(request, "auctions/category.html", {
        'Lists': Listings_x
        
    })

@login_required
def watchlist(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            current_user = request.user
            user_watchlist = User_Watchlist.objects.get(user=current_user)
            watch_list = user_watchlist.listing.all()
            return render(request, "auctions/watchlist.html", {
                "watch_list": watch_list
            })
        else:
            return render(request, "auctions/watchlist.html", {
                "message": "Please login to view your watchlist."
            })
    else:
        return render(request, "auctions/watchlist.html", {
            "message": "Invalid request method."
        })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
