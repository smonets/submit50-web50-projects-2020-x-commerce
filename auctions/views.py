from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Category
from .forms import ListingForm



def index(request):
    listings = Listing.objects.order_by('date_added')
    context = {'listings': listings}
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
    if request.method != "POST":
        listing = Listing.objects.get(id=listing_id)
        user = request.user
        watching = user.watch_listings.all()
        if listing in watching:
            show = False
        else:
            show = True
        context = {'listing': listing, 'show': show}
        return render(request, "auctions/listing.html", context)
    else:
        listing = Listing.objects.get(id=listing_id)
        user = request.user
        user.watch_listings.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))



def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "auctions/categories.html", context)


def category_items(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = category.listings.all()
    context = {'category': category, 'listings': listings}
    return render(request, "auctions/category_id.html", context)


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




