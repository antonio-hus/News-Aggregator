###################
# IMPORTS SECTION #
###################
import datetime

# Django Defined
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers


# Rest Framework Defined
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# User Defined
from .models import User, Media, Category, Tag, NewsSource, Article
from .utils import periodicUpdate


#######################
# USER INFO ENDPOINTS #
#######################

@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'is_authenticated': True,
            'username': user.username,
        })
    return Response({
        'is_authenticated': False,
        'username': 'N/A',
    })


##########################
# ARTICLE INFO ENDPOINTS #
##########################

@api_view(['GET'])
def get_all_news(request):
    articles = Article.objects.all()
    articles_json = serializers.serialize('json', articles)
    return Response({
        "article_list": articles_json,
    })


############################
# AUTHENTICATION ENDPOINTS #
############################

@api_view(['POST'])
def login_view(request):
    # Attempt to sign user in
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful."})
    else:
        return Response({"message": "Invalid username and/or password."}, status=400)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message": "Logged out successfully."})


@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")

    # Ensure password matches confirmation
    password = request.data.get("password")
    confirmation = request.data.get("confirmation")
    if password != confirmation:
        return Response({"message": "Passwords must match."}, status=400)

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except IntegrityError:
        return Response({"message": "Username already taken."}, status=400)
    login(request, user)
    return Response({"message": "Registration successful."})
