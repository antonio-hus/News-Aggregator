###################
# IMPORTS SECTION #
###################
import datetime

# Django Defined
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.db.models import Q


# Rest Framework Defined
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination

# User Defined
from .models import User, Media, Category, Tag, NewsSource, Article
from .serializers import ArticleSerializer, NewsSourceSerializer, UserProfileSerializer, UserSerializer


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_data(request):
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


##########################
# ARTICLE INFO ENDPOINTS #
##########################

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_articles(request):
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(tags__title__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()
    else:
        articles = Article.objects.none()

    # Serialize queryset using DRF serializer
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_article(request, articleId: int):
    article = Article.objects.get(id=articleId)

    # Serialize article using DRF serializer
    serializer = ArticleSerializer(article, context={'request': request})
    return Response(serializer.data)


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
            articles = articles.filter(tags__title=tag_title)
        except Tag.DoesNotExist:
            return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


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
            articles = articles.filter(tags__title=tag_title)
        except Tag.DoesNotExist:
            return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_read_later_news(request):
    try:
        user = request.user
        articles = Article.objects.filter(read_later_by=user)

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
                articles = articles.filter(tags__title=tag_title)
            except Tag.DoesNotExist:
                return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    except ObjectDoesNotExist as e:
        return Response({"error": str(e)}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_news(request):
    try:
        user = request.user
        articles = Article.objects.filter(favorited_by=user)

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
                articles = articles.filter(tags__title=tag_title)
            except Tag.DoesNotExist:
                return Response({"error": f"Tag '{tag_title}' does not exist."}, status=404)

        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    except ObjectDoesNotExist as e:
        return Response({"error": str(e)}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_publisher_news(request, name: str):
    try:
        publisher = NewsSource.objects.get(name=name)
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)

    articles = Article.objects.filter(publisher=publisher)
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_publisher_data(request, name: str):
    try:
        publisher = NewsSource.objects.get(name=name)
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)

    # Serialize the publisher data
    serializer_context = {'request': request}
    publisher_json = NewsSourceSerializer(publisher, context=serializer_context)

    # Check if user is authenticated and add follow status
    follow_status = False
    if request.user.is_authenticated:
        follow_status = request.user.is_following(publisher)

    # Return response with publisher data and follow status
    return Response({
        "publisher": publisher_json.data,
        "is_following": follow_status,
        "is_authenticated": request.user.is_authenticated,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_publishers(request):
    publishers = NewsSource.objects.all()
    serializer = NewsSourceSerializer(publishers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_category_news(request, title: str):
    try:
        category = Category.objects.get(title=title)
    except Category.DoesNotExist:
        return Response({"error": f"Category '{title}' does not exist."}, status=404)

    articles = Article.objects.filter(category=category)
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_tagged_news(request, title: str):
    try:
        tag = Tag.objects.get(title=title)
    except Tag.DoesNotExist:
        return Response({"error": f"Tag '{title}' does not exist."}, status=404)

    articles = Article.objects.filter(tags=tag)
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


#####################################
# ARTICLE RECOMMENDATIONS ENDPOINTS #
#####################################

# Collaborative Filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_articles_by_users(request):
    user = request.user

    # Find articles favorited by users who have also favorited articles that this user has favorited
    favorited_articles_ids = user.favorite_articles.values_list('id', flat=True)
    similar_users = User.objects.filter(favorite_articles__in=favorited_articles_ids).exclude(id=user.id).distinct()
    recommended_articles = Article.objects.filter(favorited_by__in=similar_users).exclude(favorited_by=user)

    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(recommended_articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


# Content Filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_articles_by_content(request):
    user = request.user

    # Get categories and tags of articles favorited by the user
    favorited_categories = user.favorite_articles.values_list('category__id', flat=True).distinct()
    favorited_tags = user.favorite_articles.values_list('tags__id', flat=True).distinct()

    # Filter articles based on favorited categories or favorited tags, and exclude those already favorited by the user
    recommended_articles = Article.objects.filter(
        Q(category__id__in=favorited_categories) | Q(tags__id__in=favorited_tags)
    ).exclude(favorited_by=user).distinct()

    # Paginate the recommended articles
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(recommended_articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


##############################
# USER INTERACTION ENDPOINTS #
##############################

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_article(request, articleId):
    try:
        article = Article.objects.get(id=articleId)
        user = request.user
        article.favorite(user)
        return Response({"message": f"User - {user.username} favorited article with id - {articleId}."})

    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfavorite_article(request, articleId):
    try:
        article = Article.objects.get(id=articleId)
        user = request.user
        article.unfavorite(user)
        return Response({"message": f"User - {user.username} unfavorited article with id - {articleId}."})

    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def readlater_article(request, articleId):
    try:
        article = Article.objects.get(id=articleId)
        user = request.user
        article.read_later(user)
        return Response({"message": f"User - {user.username} read later article with id - {articleId}."})

    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unreadlater_article(request, articleId):
    try:
        article = Article.objects.get(id=articleId)
        user = request.user
        article.unread_later(user)
        return Response({"message": f"User - {user.username} unread later article with id - {articleId}."})

    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_publisher(request, name):
    try:
        publisher = NewsSource.objects.get(name=name)
        user = request.user
        user.follow(publisher)
        return Response({"message": f"You followed {publisher.name}."})
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_publisher(request, name):
    try:
        publisher = NewsSource.objects.get(name=name)
        user = request.user
        user.unfollow(publisher)
        return Response({"message": f"You unfollowed {publisher.name}."})
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)


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
