from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Auction_listings, Bidding_Book, Auction_categories, User_Watchlist, Comments, Closed_Auctions, Bids
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
            return HttpResponseRedirect(reverse("active_listing"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("active_listing"))


# login req
@login_required
def create_new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid_price = request.POST["starting_bid_price"]
        url = request.POST["url"]
        category = Auction_categories.objects.get(name=str(request.POST["category"]))
        
        new_listing =Auction_listings.objects.create(
            title = title,
            description = description,
            photo = url,
            current_price = starting_bid_price,
            category = category
        )
        bidding_book, created = Bidding_Book.objects.get_or_create(user=request.user)
        bidding_book.listing.add(new_listing)

        return HttpResponseRedirect(reverse("active_listing"))

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
    bids = x_listing.bid.all()
    user_initiated_bid = False
    if request.user.is_authenticated:
        current_user = request.user
        user_bidding_listings = Bidding_Book.objects.filter(user=current_user, listing=x_listing)
        if user_bidding_listings.exists():
            user_initiated_bid = True

        try:
            current_user_watchlist = User_Watchlist.objects.get(user=current_user)
        except User_Watchlist.DoesNotExist:
            current_user_watchlist =User_Watchlist.objects.create(user=current_user)

        if User_Watchlist.objects.filter(user=current_user, listing=x_listing).exists():
            is_in_watchlist = True
            if request.method == "POST":
                current_user_watchlist.listing.remove(x_listing)
                return HttpResponseRedirect(reverse("watchlist"))
            return render(request, "auctions/listing.html", {
                "Listing": x_listing,
                "Comments": comments,
                "is_in_watchlist": is_in_watchlist,
                "user_initiated_bid": user_initiated_bid
            })
        else:
            if request.method == "POST":   
                current_user_watchlist.listing.add(x_listing)
                return HttpResponseRedirect(reverse("watchlist"))

    return render(request, "auctions/listing.html", {
        "Listing": x_listing,
        "Comments": comments,
        "bids": bids,
        "user_initiated_bid": user_initiated_bid
        
    })

def closed_listing(request, list):
    close_list = Auction_listings.objects.get(title=str(list))
    
    Winner_price = close_list.current_price

    bid_user = Bids.objects.get(current_bid_price=Winner_price)
    Closed_Auctions.objects.create(
        title = close_list.title,
        description = close_list.description,
        photo = close_list.photo
    )
    X_list = Closed_Auctions.objects.get(title=str(list))
    
    close_list.delete()
    return render(request, "auctions/closed_auctions.html",{
        "Listing": X_list,
        "Price": bid_user
    })

def bid(request, list):
    if request.method == "POST":
        current_user = request.user
        bid_x = int(request.POST.get("Bid"))
        listing = Auction_listings.objects.get(title=str(list))
        highest_bid = listing.current_price
        if int(bid_x) > int(highest_bid):
            bid_ = Bids.objects.create(current_bid_price=bid_x, user=current_user)
            listing.bid.add(bid_)
            listing.current_price = bid_x
            listing.save()
        else:
            return HttpResponseRedirect(reverse('active_listing'))

        return HttpResponseRedirect(reverse('active_listing'))


def comment(request, list):
    if request.method == "POST":
        comment_x = request.POST.get("Add_Comment")
        listing = Auction_listings.objects.get(title=str(list))
        comment_ = Comments.objects.create(comment=comment_x)
        listing.comment.add(comment_)
        
        return HttpResponseRedirect(reverse('active_listing'))  




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


