from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

from .models import *


def index(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            # Create post form and save post
            post_content = CreatePost(request.POST)
            # print(post_content)
            if post_content.is_valid():
                user = User.objects.get(username=request.user)
                # print(user)
                user_post_content = post_content.save(commit=False)
                user_post_content.user = user
                user_post_content.save()

        # User info for the right container
        all_users = User.objects.all()
        users = []
        present_user = User.objects.get(username=request.user)
        for all_user in all_users:
            if all_user != present_user and all_user.username != "admin":
                users.append(all_user)

        # Get all posts by order
        posts = Post.objects.all().order_by("-timestamp")
        # Post pagination
        p = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = p.get_page(page_number)
        return render(
            request,
            "network/index.html",
            {
                "posts": posts,
                "post": CreatePost(),
                "users": users,
                "page_obj": page_obj,
            },
        )
    else:
        return HttpResponseRedirect(reverse("login"))


@login_required
def following_index(request):

    # Get follow objects for the present user
    follows = Follow.objects.filter(user=request.user.id)
    # print(follows)

    followings = []
    following_users = []

    for follow in follows:
        followings.append(follow.following)
        # print(followings)

    # Get rid of None
    for following in followings:
        if following is not None:
            following_users.append(following)
    # Get all posts by users that the current user follows
    posts = []

    # User info for the right container
    all_users = User.objects.all()
    users = []
    present_user = User.objects.get(username=request.user)
    for all_user in all_users:
        if all_user != present_user and all_user.username != "admin":
            users.append(all_user)

    for following_user in following_users:
        # print(following_user)
        following_posts = Post.objects.filter(user=following_user.id).order_by(
            "-timestamp"
        )
        posts += following_posts
    # Order those posts
    posts.sort(key=lambda r: r.timestamp, reverse=True)

    p = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(
        request,
        "network/following.html",
        {
            "posts": posts,
            "post": CreatePost(),
            "page_obj": page_obj,
            "users": users,
        },
    )


@login_required
def likes(request, post_id, user_id):

    if request.method == "POST":
        # Get JS post data
        data = json.loads(request.body)
        # print(data)
        if data.get("post") is not None:
            post_id = data.get("post")
            # print(post_id)
        if data.get("user") is not None:
            user_id = data.get("user")
            # print(user_id)
        post = Post.objects.get(pk=post_id)
        user = User.objects.get(pk=user_id)

        post_likes = Like.objects.filter(post=post.id)
        likers = []
        if post_likes:
            for e in post_likes:
                likers.append(e.user)

            if user not in likers:
                like = Like(post=post, user=user)
                like.save()
                print(like)
                post.like_count += 1
                post.save()
                print(post.like_count)

                # print("likes")
            else:
                print(e)
                e.delete()
                print(e)
                post.like_count -= 1
                post.save()
                print(post.like_count)
        else:
            like = Like(post=post, user=user)
            post.like_count += 1

            like.save()
            print(like)
            post.save()
            print(post.like_count)

        likes = Like.objects.filter(post=post_id)
        # print(likes)
        return JsonResponse([like.serialize() for like in likes], safe=False)

    # Post must be via GET or PUT
    else:
        return JsonResponse({"error": "GET or POST request required."}, status=400)


@login_required
def edit(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # print(post)

    if request.method == "PUT":
        # Get edit info from JS
        data = json.loads(request.body)
        # print(data)
        if data.get("content") is not None:
            post.content = data["content"]

        post.save()
        # print(post.content)
        # print(post)
        return HttpResponse(status=204)

    # Post must be via GET or PUT
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
def user_profile(request, username):
    e_followings = []

    user = User.objects.get(username=username)
    # print(request.user)

    # Get follow objects of the current user
    user_follows = Follow.objects.filter(user=request.user.id)
    # print(user_follows)
    for e in user_follows:
        e_followings.append(e.following)
        print(e_followings)

    # Present user follows
    if request.method == "POST":

        # Toggle between follow and unfollow
        if user not in e_followings:
            # print(user)
            new_following = Follow(user=request.user, following=user)
            new_follower = Follow(user=user, follower=request.user)
            new_following.save()
            new_follower.save()

        else:
            delete_following = Follow.objects.get(user=request.user, following=user)
            delete_follower = Follow.objects.get(user=user, follower=request.user)
            delete_following.delete()
            delete_follower.delete()

        return HttpResponseRedirect(reverse("user_profile", args=(username,)))

    # print(username)

    # Get posts of the current user
    id = user.id
    posts = Post.objects.filter(user=id).order_by("-timestamp")

    p = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    # print(page_obj)

    # User info for the right container
    all_users = User.objects.all()
    users = []
    present_user = User.objects.get(username=request.user)
    for all_user in all_users:
        if all_user != present_user and all_user.username != "admin":
            users.append(all_user)

    # Count followers and followings
    followers = []
    followers_count = 0
    follows = Follow.objects.filter(user=id)
    # print(follows)
    for follow in follows:
        followers.append(follow.follower)
        # print(followers)

    for follower in followers:
        if follower is not None:
            followers_count += 1

    followings = []
    followings_count = 0
    # print(follows)
    for follow in follows:
        followings.append(follow.following)
        # print(followings)

    for following in followings:
        if following is not None:
            followings_count += 1

    return render(
        request,
        "network/profile.html",
        {
            "posts": posts,
            "post": CreatePost(),
            "users": users,
            "user": user,
            "page_obj": page_obj,
            "followers_count": followers_count,
            "followings_count": followings_count,
            "e_followings": e_followings,
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
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


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
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
