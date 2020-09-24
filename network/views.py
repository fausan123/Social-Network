import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts, Likes, Following
from .forms import CreatePost


def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreatePost(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                post = Posts.objects.create(content=content, user=request.user)
                post.save()

    posts = Posts.objects.all().order_by('-date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if paginator.num_pages > 1:
        is_paginated = True
    else:
        is_paginated = False
    return render(request, "network/index.html", {
        'form': CreatePost(), 'page_obj': page_obj, 'is_paginated': is_paginated
    })


def profile_view(request, id):
    user = User.objects.get(id=id)
    posts = user.posts.all().order_by('-date')
    if request.user.is_authenticated:
        following_user = user.followers.filter(
            follower=request.user, user=user)
    else:
        following_user = None

    if request.method == 'POST':
        image = request.FILES["image"]
        user.image = image
        user.save()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if paginator.num_pages > 1:
        is_paginated = True
    else:
        is_paginated = False
    return render(request, "network/profile.html", {
        'profile': user, 'page_obj': page_obj,
        'is_paginated': is_paginated, 'following_user': following_user
    })


@login_required
def following_view(request):
    posts = []
    followings = request.user.following.all()
    for following in followings:
        f_posts = following.user.posts.all()
        for post in f_posts:
            posts.append(post)
    posts = sorted(posts, key=lambda k: k.date, reverse=True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if paginator.num_pages > 1:
        is_paginated = True
    else:
        is_paginated = False
    return render(request, "network/following.html", {
        'page_obj': page_obj, 'is_paginated': is_paginated
    })


@csrf_exempt
@login_required
def get_or_like_post(request, post_id):
    post = Posts.objects.get(pk=post_id)

    if request.method == 'GET':
        if request.user == post.user:
            return JsonResponse({'content': post.content})
        else:
            return JsonResponse({
                "error": "Action not authorized",
                "status": 401
            }, status=401)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("liked") is not None:
            if data["liked"]:
                post.post_likes.add(request.user)
                like = Likes.objects.create(post=post, user=request.user)
                like.save()
            else:
                post.post_likes.remove(request.user)
                like = Likes.objects.filter(
                    post=post, user=request.user).first()
                like.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "GET or PUT request required.",
            "status": 400
        }, status=400)


@csrf_exempt
@login_required
def follow_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("follow") is not None:
            if data["follow"]:
                follow = Following.objects.create(
                    user=user, follower=request.user)
                follow.save()
            else:
                follow = Following.objects.get(
                    user=user, follower=request.user)
                follow.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required.",
            "status": 400
        }, status=400)


@csrf_exempt
@login_required
def edit_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required.", "status": 400}, status=400)

    data = json.loads(request.body)
    id = data["id"]
    content = data["content"]

    post = Posts.objects.get(id=id)
    if post.user != request.user:
        return JsonResponse({
            "error": "Action not authorized, You are not allowed to edit other user's post",
            "status": 401
        }, status=401)
    post.content = content
    post.edited = True
    post.save()

    return JsonResponse({"message": "Post edited successfully.", "status": 201}, status=201)


@csrf_exempt
@login_required
def edit_bio(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required.", "status": 400}, status=400)
    data = json.loads(request.body)
    id = data["id"]
    bio = data["bio"]
    user = User.objects.get(id=id)
    if user != request.user:
        return JsonResponse({
            "error": "Action not authorized, You are not allowed to edit other user's bio",
            "status": 401
        }, status=401)
    user.bio = bio
    user.save()
    return JsonResponse({"message": "Bio edited successfully.", "status": 201}, status=201)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("profile", kwargs={'id': user.id}))
    else:
        return render(request, "network/register.html")
