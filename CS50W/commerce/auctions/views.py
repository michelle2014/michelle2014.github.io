from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import *


# active listing page
def index(request):
    categories = Category.objects.all()

    # get all listings with the newest on the top
    forms = Listing.objects.filter(active=True).order_by("-timestamp")

    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        pass

    # as remove button if in watchlist, otherwise as add button

    for form in forms:
        current_price = form.current_price

    # print(form.title)
    # print(image_url)
    # print(current_price)

    return render(
        request,
        "auctions/index.html",
        {
            "forms": forms,
            "categories": categories,
        },
    )


# all the active and closed listings in all categories
def departments(request):
    categories = Category.objects.all()

    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        pass

    # get all listings with the newest on the top
    all_forms = Listing.objects.all().order_by("-timestamp")

    for all_form in all_forms:
        current_price = all_form.current_price
        image_url = all_form.image_url
        # print(current_price)
    return render(
        request,
        "auctions/index.html",
        {
            "all_forms": all_forms,
            "categories": categories,
        },
    )


# display listing by category
def category(request, category):
    categories = Category.objects.all()

    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        pass

    # get listing of a specific category
    cate = Category.objects.get(title=category)
    id = cate.id
    # print(cate.title)

    # get all the active listings in a specific category with the newest on the top
    forms = Listing.objects.filter(category=id, active=True).order_by("-timestamp")
    return render(
        request,
        "auctions/index.html",
        {
            "forms": forms,
            "categories": categories,
            "cate": cate,
        },
    )


# display a user's watchlist
def watchlist_view(request):
    categories = Category.objects.all()

    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        pass

    forms = user.watchlist.all().order_by("-timestamp")

    return render(
        request,
        "auctions/watchlist.html",
        {
            "forms": forms,
            "categories": categories,
        },
    )


# create a listing
def create(request):
    categories = Category.objects.all()

    if request.method == "POST":
        # Get the form with all the data and files submitted
        form = CreateForm(request.POST, request.FILES or None)

        # Get the username of the login user
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            pass

        if form.is_valid():

            # add user info to the form submitted
            user_form = form.save(commit=False)
            user_form.user = user

            # save the form and return to the index page to display listings
            user_form.save()

            # display a success message when create a listing successfully
            messages.success(request, "Listing created successfullly.")

            return HttpResponseRedirect(reverse("index"))

    # If request method is get, display the form
    return render(
        request,
        "auctions/create.html",
        {
            "form": CreateForm(),
            "categories": categories,
        },
    )


# diplay a listing page when no user is logged in
def listing_view(request, title):

    # if get a listing page
    categories = Category.objects.all()
    # print(title)

    # Get all the forms submitted
    forms = Listing.objects.all()

    all_forms = Listing.objects.all()

    # Get the listing with the title
    listing = Listing.objects.get(title=title)
    # print(listing)

    # get the highest bid for a listing
    # get the highest bid for a listing
    highest_price = Bid.objects.filter(title=title).order_by("-bid_price").first()
    # print(highest_price)

    if highest_price is not None:
        listing.current_price = highest_price.bid_price

    # else set starting price as the current price
    else:
        listing.current_price = listing.starting_price
        listing.save()

    # Get all comments and order by time commented
    comments = Comment.objects.filter(title=title).order_by("-comment_at")

    # if there is a highest price for a listing, set it as the current price

    return render(
        request,
        "auctions/listing.html",
        {
            "forms": forms,
            "comments": comments,
            "bid": CreateBid,
            "categories": categories,
            "comment": CreateComment(),
            "listing": listing,
        },
    )


@login_required
# display a listing page when a user logged in
# place bid, close an auction or add to or remove from the watchlist
def my_listing_view(request, title):

    # if get a listing page
    categories = Category.objects.all()

    print(title)

    # Get all the forms submitted
    forms = Listing.objects.all()

    all_forms = Listing.objects.all()

    # Get the listing with the title
    listing = Listing.objects.get(title=title)
    # print(listing)

    # get the highest bid for a listing
    highest_price = Bid.objects.filter(title=title).order_by("-bid_price").first()
    # print(highest_price)

    if highest_price is not None:
        listing.current_price = highest_price.bid_price

    # else set starting price as the current price
    else:
        listing.current_price = listing.starting_price

    creator = listing.user
    # print(creator)

    # Create a comment form
    comment = CreateComment()

    # Get all comments and order by time commented
    comments = Comment.objects.filter(title=title).order_by("-comment_at")

    # create a bid form
    bid = CreateBid()

    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        pass

    value = False

    # as remove button if in watchlist, otherwise as add button
    watchlists = user.watchlist.all()
    for watchlist in watchlists:
        # print(watchlist.title)
        if watchlist.title == listing.title:
            value = True
        else:
            value = False

    # if place a bid, close an auction or add to or remove from the watchlist
    if request.method == "POST":

        # If comment
        if request.POST.get("comment"):
            # Get comment text
            comment_text = CreateComment(request.POST)
            # print(comment_text)
            if comment_text.is_valid():
                if creator != user:
                    user_comment_text = comment_text.save(commit=False)
                    user_comment_text.user = user
                    user_comment_text.title = title
                    user_comment_text.save()
                    # print(user_comment_text)

                    return render(
                        request,
                        "auctions/my_listing.html",
                        {
                            "forms": forms,
                            "listing": listing,
                            "comments": comments,
                            "bid": CreateBid(),
                            "creator": creator,
                            "user": user,
                            "comment": CreateComment(),
                            "categories": categories,
                        },
                    )
                # if commentor is the creator, display an error message
                else:
                    return render(
                        request,
                        "auctions/my_listing.html",
                        {
                            "forms": forms,
                            "listing": listing,
                            "comments": comments,
                            "comment": CreateComment(),
                            "bid": CreateBid(),
                            "creator": creator,
                            "user": user,
                            "categories": categories,
                            "message": "User cannot comment on listings created by their own.",
                        },
                    )

        # If bid
        elif request.POST.get("place_bid"):
            # Get bid price from user input
            bids = CreateBid(request.POST)

            if bids.is_valid():
                if creator != user:
                    user_bid = bids.save(commit=False)
                    user_bid.user = user
                    user_bid.title = title
                    # save the form and return to the index page to display listings
                    user_bid.save()

                    bid_price = user_bid.bid_price

                    # if bid price is valid, save it to the database
                    if bid_price > listing.current_price:
                        listing.current_price = bid_price

                        # get how many bids have been placed
                        counts = Bid.objects.filter(title=title)

                        for count in counts:
                            if count.bid_price > highest_price.bid_price:
                                print("true")
                                listing.bid_count += 1
                        # print(bid_count)

                        listing.save()
                        # print(listing.current_price)

                        # print(listing)
                        return render(
                            request,
                            "auctions/my_listing.html",
                            {
                                "forms": forms,
                                "listing": listing,
                                "bid": CreateBid(),
                                "comments": comments,
                                "comment": CreateComment(),
                                "creator": creator,
                                "user": user,
                                "categories": categories,
                                "listing.bid_count": listing.bid_count,
                            },
                        )

                    # if the bid is negative or lower than the current price
                    else:
                        return render(
                            request,
                            "auctions/my_listing.html",
                            {
                                "forms": forms,
                                "listing": listing,
                                "bid": CreateBid(),
                                "comments": comments,
                                "comment": CreateComment(),
                                "creator": creator,
                                "user": user,
                                "categories": categories,
                                "message": "Bid price must be a positive number higher than the current price.",
                            },
                        )

                # if bidder is the creator, display an error message
                else:
                    return render(
                        request,
                        "auctions/my_listing.html",
                        {
                            "forms": forms,
                            "listing": listing,
                            "bid": CreateBid(),
                            "comments": comments,
                            "comment": CreateComment(),
                            "creator": creator,
                            "user": user,
                            "categories": categories,
                            "message": "User cannot bid on listings created by their own.",
                        },
                    )

            # if bid is other than a number
            else:
                return render(
                    request,
                    "auctions/my_listing.html",
                    {
                        "forms": forms,
                        "listing": listing,
                        "bid": CreateBid(),
                        "comments": comments,
                        "comment": CreateComment(),
                        "creator": creator,
                        "categories": categories,
                        "user": user,
                        "message": "Bid price must be a number.",
                    },
                )

        # if to close an auction
        elif request.POST.get("close"):
            bid_close = request.POST["close"]

            listing.active = False
            # print(listing.active)

            # get winner info
            winner = str(Bid.objects.get(bid_price=listing.current_price).user)
            # print(winner)
            listing.winner = winner
            listing.save()
            # print(listing.winner)

            return render(
                request,
                "auctions/my_listing.html",
                {
                    "forms": forms,
                    "listing": listing,
                    "comment": comment,
                    "comments": comments,
                    "creator": creator,
                    "user": user,
                    "categories": categories,
                    "listing.winner": listing.winner,
                },
            )

        # If watchlist
        else:

            try:
                user = User.objects.get(username=request.user)
            except User.DoesNotExist:
                pass

            # if already in user's watchlist, remove it
            if listing in user.watchlist.all():
                user.watchlist.remove(listing)
                user.save()

            # else add it
            else:
                user.watchlist.add(listing)
                user.save()

            forms = user.watchlist.all()

            return HttpResponseRedirect(reverse("watchlist_view"))

    return render(
        request,
        "auctions/my_listing.html",
        {
            "forms": forms,
            "listing": listing,
            "comment": comment,
            "comments": comments,
            "bid": bid,
            "creator": creator,
            "user": user,
            "value": value,
            "categories": categories,
            "comment": CreateComment(),
        },
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
