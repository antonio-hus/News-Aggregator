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

    # Optional filters
    category_title = request.query_params.get('category')
    tag_title = request.query_params.get('tag')

    if category_title:
        try:
            category = Category.objects.get(title=category_title)
            articles = articles.filter(category=category)
        except Category.DoesNotExist:
            return Response({"error": f"Category '{category_title}' does not exist."}, status=404)

    if tag_title:
        try:
            tag = Tag.objects.get(title=tag_title)
            articles = articles.filter(tags=tag)
        except Tag.DoesNotExist:
            return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

    articles_json = serializers.serialize('json', articles)
    return Response({
        "article_list": articles_json,
    })


@api_view(['GET'])
def get_following_news(request):
    # Get the current user & news sources that the user follows
    user = request.user
    followed_sources = user.followed_news_sources.all()

    # Filter articles based on followed news sources
    articles = Article.objects.filter(publisher__in=followed_sources)

    # Optional filters
    category_title = request.query_params.get('category')
    tag_title = request.query_params.get('tag')

    if category_title:
        try:
            category = Category.objects.get(title=category_title)
            articles = articles.filter(category=category)
        except Category.DoesNotExist:
            return Response({"error": f"Category '{category_title}' does not exist."}, status=404)

    if tag_title:
        try:
            tag = Tag.objects.get(title=tag_title)
            articles = articles.filter(tags=tag)
        except Tag.DoesNotExist:
            return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

    articles_json = serializers.serialize('json', articles)
    return Response({
        "article_list": articles_json,
    })


@api_view(['GET'])
def get_publisher_news(request, name: str):
    try:
        publisher = NewsSource.objects.get(name=name)
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)

    articles = Article.objects.filter(publisher=publisher)
    articles_json = serializers.serialize('json', articles)

    return Response({
        "article_list": articles_json,
    })


@api_view(['GET'])
def get_category_news(request, title: str):
    try:
        category = Category.objects.get(title=title)
    except Category.DoesNotExist:
        return Response({"error": f"Category '{title}' does not exist."}, status=404)

    articles = Article.objects.filter(category=category)
    articles_json = serializers.serialize('json', articles)

    return Response({
        "article_list": articles_json,
    })


@api_view(['GET'])
def get_tagged_news(request, title: str):
    try:
        tag = Tag.objects.get(title=title)
    except Tag.DoesNotExist:
        return Response({"error": f"Tag '{title}' does not exist."}, status=404)

    articles = Article.objects.filter(tags=tag)
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
