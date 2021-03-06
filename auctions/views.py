from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid
from .forms import ListingForm, CommentForm, BidForm



def index(request):
    listings = Listing.objects.order_by('-date_added')
    active_listings = []
    for listing in listings:
        if listing.active == True:
            active_listings.append(listing)
    context = {'listings': active_listings}
    return render(request, "auctions/index.html", context)


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


@login_required
def new(request):

    if request.method == 'POST':
        form = ListingForm(data=request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing.save()
            return redirect('index')
    else:
        form = ListingForm()
        context = {'form': form}
        return render(request, "auctions/new.html", context)



def listing(request, listing_id):
    user = request.user
    users = User.objects.all()
    listing = Listing.objects.get(id=listing_id)
    comments = listing.comment_set.all()
    highest = listing.starting_bid
    bids = listing.bid_set.all()
    highest_owner = "owner"
    show_closing = False
    for bid in bids:
        if bid.bid > highest:
            highest = bid.bid
            highest_owner = bid.owner
    if user in users:
        watching = user.watch_listings.all()
        if request.method != "POST":
            if listing.owner == user and listing.active == True:
                show_closing = True
            if listing in watching:
                show = False
            else:
                show = True
            context = {'listing': listing, 'show': show, 'comments': comments, 'highest_bid': highest,
                       'highest_owner': highest_owner, 'show_closing': show_closing, 'user': user}
            return render(request, "auctions/listing.html", context)
        else:
            if 'watchlist' in request.POST:
                if listing in watching:
                    user.watch_listings.remove(listing)
                else:
                    user.watch_listings.add(listing)
            if 'active' in request.POST:
                listing.active = False
                listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        signed = True
        context = {'listing': listing, 'signed': signed, 'comments': comments,'highest_bid': highest,
                   'highest_owner': highest_owner}
        return render(request, "auctions/listing.html", context)

@login_required
def comment(request, listing_id):
    if request.method != "POST":
        listing = Listing.objects.get(id=listing_id)
        form = CommentForm()
        context = {'listing': listing, 'form': form}
        return render(request, "auctions/comment.html", context)
    else:
        listing = Listing.objects.get(id=listing_id)
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.listing = listing
            new_comment.owner = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


@login_required
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)


@login_required
def category_items(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = category.listings.all()
    context = {'category': category, 'listings': listings}
    return render(request, "auctions/category_id.html", context)


@login_required
def watchlist(request):
    if request.method != "POST":
        user = request.user
        watching = user.watch_listings.all()
        context = {'user': user, 'watchings': watching}
        return render(request, "auctions/watching.html", context)
    else:
        user = request.user
        watch_id = int(request.POST["submit"])
        user.watch_listings.remove(watch_id)
        return HttpResponseRedirect(reverse("watchlist"))


@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    if request.method != "POST":
        form = BidForm()
        context = {'form': form, 'listing': listing}
        return render(request, "auctions/bid.html", context)
    else:
        form = BidForm(data=request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.listing = listing
            new_bid.owner = user
            bids = listing.bid_set.all()
            if new_bid.bid < listing.starting_bid:
                error = "Your bid is too small"
                context = {'form': form, 'listing': listing, 'error': error}
                return render(request, "auctions/bid.html", context)
            else:
                for bid in bids:
                    if new_bid.bid < bid.bid:
                        error = "Your bid is too small"
                        context = {'form': form, 'listing': listing, 'error': error}
                        return render(request, "auctions/bid.html", context)
                new_bid.save()
                listing.highest = new_bid.bid
                listing.save()
                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))






