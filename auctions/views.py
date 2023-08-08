from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", dict(activeListings=activeListings, categories=allCategories))


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


def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        # User identification
        currentUser = request.user

        categoryData = Category.objects.get(categoryName=category)

        bid = Bid(bid=int(starting_bid), user=currentUser)
        bid.save()

        newListing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            starting_bid=bid,
            category=categoryData,
            owner=currentUser
        )
        newListing.save()
        return HttpResponseRedirect(reverse("index"))


def categoryDisplay(request):
    categoryData = Category.objects.all()
    return render(request, 'auctions/categoryDisplay.html', {'categoryData': categoryData, })


def category(request, category_id):
    categoryData = Category.objects.get(pk=category_id)
    activeListings = Listing.objects.filter(isActive=True, category=categoryData)
    allCategories = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories": allCategories,
        "category": categoryData,
        "activeListings": activeListings
    })


def listing(request, listing_id):
    listingData = Listing.objects.get(pk=listing_id)
    inWatchlist = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "inWatchlist": inWatchlist,
        "comments": allComments,
        "isOwner": isOwner
    })


def addWatchlist(request, listing_id):
    listingData = Listing.objects.get(pk=listing_id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


def removeWatchlist(request, listing_id):
    listingData = Listing.objects.get(pk=listing_id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })


def addComment(request, listing_id):
    listingData = Listing.objects.get(pk=listing_id)
    currentUser = request.user
    message = request.POST["newComment"]

    newComment = Comments(
        author=currentUser,
        listing=listingData,
        message=message
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


def addBid(request, listing_id):
    newBid = request.POST["newBid"]
    listingData = Listing.objects.get(pk=listing_id)
    inWatchlist = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    if int(newBid) > listingData.starting_bid.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.starting_bid = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bet Successful",
            "inWatchlist": inWatchlist,
            "comments": allComments,
            "update": True,
            "isOwner": isOwner,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bet Failed",
            "inWatchlist": inWatchlist,
            "comments": allComments,
            "update": False,
            "isOwner": isOwner,
        })


def closeAuction(request, listing_id):
    listingData = Listing.objects.get(pk=listing_id)
    listingData.isActive = False
    listingData.save()
    listingData = Listing.objects.get(pk=listing_id)
    inWatchlist = request.user in listingData.watchlist.all()
    allComments = Comments.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "inWatchlist": inWatchlist,
        "comments": allComments,
        "isOwner": isOwner,
        "update": True,
        "message": "Auction Closed",
    })

