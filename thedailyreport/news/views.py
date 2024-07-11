###################
# IMPORTS SECTION #
###################

# Django Defined
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

# Rest Framework Defined
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# User Defined
from .models import User
from .web_scrapers import DIGI24


#######################
# USER INFO ENDPOINTS #
#######################

def get_user(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse({
            'is_authenticated': True,
            'username': user.username,
        })
    return JsonResponse({
        'is_authenticated': False,
        'username': 'N/A',
    })


##########################
# ARTICLE INFO ENDPOINTS #
##########################

def get_all_news(request):

    article_list = DIGI24.scrape_news.get()
    # Scrape All Other Sites

    return JsonResponse({
        "article_list": article_list
    })


############################
# AUTHENTICATION ENDPOINTS #
############################


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
            return render(request, "news/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")


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
            return render(request, "news/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "news/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/register.html")