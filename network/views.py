from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required


@login_required
def follow(request, user_pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(
            [
                "POST",
            ],
            "405: Method not allowed. Only 'POST' method is permitted for this resource",
        )
    try:
        req_user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        raise Http404
    user = request.user
    if req_user in user.following.all():
        user.following.remove(req_user)
        msg = "Unfollow successfull"
    else:
        user.following.add(req_user)
        msg = "Follow successfull"
    user.save()
    return JsonResponse({"msg": msg})


@login_required
def like(request, post_pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(
            [
                "POST",
            ],
            "405: Method not allowed. Only 'POST' method is permitted for this resource",
        )
    post = Post.objects.get(post=post_pk)
    user = request.user
    if user in post.liked_by.all():
        post.liked_by.remove(user)
        msg_addon = "un"
    else:
        post.liked_by.add(request.user)
        msg_addon = ""
    post.save()
    return JsonResponse(
        {"msg": f"Post {post_pk} succesfully {msg_addon}liked by {request.user.pk}"}
    )


def following(request):
    posts_list = Post.objects.filter(author__in=request.user.follows.all())
    return displayPosts(request, posts_list)


def profile(request, user_pk):
    try:
        req_user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        raise Http404
    posts_list = Post.objects.filter(author=req_user)
    page_obj = paginate_posts(request, posts_list)
    return render(
        request, "network/profile.html", {"req_user": req_user, "page_obj": page_obj}
    )


def index(request):
    posts_list = Post.objects.all()
    return displayPosts(request, posts_list)


def displayPosts(request, posts_list):
    page_obj = paginate_posts(request, posts_list)
    return render(request, "network/index.html", {"page_obj": page_obj})


def paginate_posts(request, posts_list):
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


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
