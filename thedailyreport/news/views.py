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
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

# User Defined
from .models import User, Media, Category, Tag, NewsSource, Article
from .serializers import ArticleSerializer


#######################
# USER INFO ENDPOINTS #
#######################

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'is_authenticated': True,
            'username': user.username,
        })
    return Response({
        'is_authenticated': False,
        'username': '',
    })


##########################
# ARTICLE INFO ENDPOINTS #
##########################

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
            articles = articles.filter(tags__title=tag_title)  # Use double underscore for ManyToMany field lookup
        except Tag.DoesNotExist:
            return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

    # Serialize queryset using DRF serializer
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
