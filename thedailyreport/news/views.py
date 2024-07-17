###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
# Django Rest Framework ( DRF ) Libraries
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
# Project Libraries
from .models import User, Media, Category, Tag, NewsSource, Article
from .serializers import ArticleSerializer, NewsSourceSerializer, UserProfileSerializer, UserSerializer


##################
# USER ENDPOINTS #
##################
# User - Basic Information
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user(request):

    # Get the current User
    user = request.user

    # Return the User's authentication status and respective username ( N/A for users not logged in )
    if user.is_authenticated:
        return Response({
            'is_authenticated': True,
            'username': user.username,
        })

    else:
        return Response({
            'is_authenticated': False,
            'username': '',
        })


# User - Extended Information
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):

    # Get current User
    user = request.user

    # Return under DRF Serializer
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


# User - Update Extended Information
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_data(request):

    # Get current User
    user = request.user

    # Get Update Form Data
    serializer = UserProfileSerializer(user, data=request.data)

    # Update Current User Data with received Form Data
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    # Return an error in case of bad Form Data
    return Response(serializer.errors, status=400)


#########################
# NEWS SOURCE ENDPOINTS #
#########################
# Publishers List
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_publishers(request):

    # Get Publishers
    publishers = NewsSource.objects.all()

    # Return under DRF Serializer
    serializer = NewsSourceSerializer(publishers, many=True)
    return Response(serializer.data)


# Publisher Data
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_publisher_data(request, name: str):

    # Get the News Source given by its name
    try:
        publisher = NewsSource.objects.get(name=name)

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

    # Return a bad status ( 404 ) response if News Source does not exist
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)


# Follow Publisher
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_publisher(request, name):
    try:

        # Get the News Source given by its name
        publisher = NewsSource.objects.get(name=name)

        # Get the current User
        user = request.user

        # Add follow relation
        user.follow(publisher)
        return Response({"message": f"You followed {publisher.name}."})

    # Return a bad status ( 404 ) response if News Source does not exist
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)


# Unfollow Publisher
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_publisher(request, name):
    try:

        # Get the News Source given by its name
        publisher = NewsSource.objects.get(name=name)

        # Get the current User
        user = request.user

        # Remove follow relation
        user.unfollow(publisher)
        return Response({"message": f"You unfollowed {publisher.name}."})

    # Return a bad status ( 404 ) response if News Source does not exist
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)


#####################
# ARTICLE ENDPOINTS #
#####################
# Paginator Class for Article Getters
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Search Articles
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_articles(request):

    # Get query from request
    query = request.GET.get('q', '')

    # If query exists, filter
    if query:

        # Check against: title, tags, categories
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(tags__title__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()

    # Else, return none
    else:
        articles = Article.objects.none()

    # Serialize queryset using DRF serializer
    serializer = ArticleSerializer(articles, many=True, context={'request': request})
    return Response(serializer.data)


# Get Article Data
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_article(request, articleId: int):

    # Get article with given id
    article = Article.objects.get(id=articleId)

    # Serialize article using DRF serializer
    serializer = ArticleSerializer(article, context={'request': request})
    return Response(serializer.data)


# Get Article List
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all_news(request):

    # Get all articles
    articles = Article.objects.all()

    # Return under DRF serialization by page
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


# Get articles from News Sources followed by the user
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

    # Return under DRF serialization by page
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


# Get articles from the user's read later list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_read_later_news(request):
    try:

        # Get the current user & read later list
        user = request.user
        articles = Article.objects.filter(read_later_by=user)

        # Return under DRF serialization by page
        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    # Return a bad response ( 404 ) if the User does not exist
    except ObjectDoesNotExist as e:
        return Response({"error": str(e)}, status=404)


# Get articles from the user's favorite list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorite_news(request):
    try:

        # Get current User and favorited articles list
        user = request.user
        articles = Article.objects.filter(favorited_by=user)

        # Return under DRF serialization by page
        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    # Return a bad response ( 404 ) if the User does not exist
    except ObjectDoesNotExist as e:
        return Response({"error": str(e)}, status=404)


# Get articles from a given News Source
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_publisher_news(request, name: str):
    try:

        # Get the News Source with the given name & articles published by it
        publisher = NewsSource.objects.get(name=name)
        articles = Article.objects.filter(publisher=publisher)

        # Return under DRF serialization by page
        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    # Return a bad response ( 404 ) if the News Source does not exist
    except NewsSource.DoesNotExist:
        return Response({"error": f"Publisher '{name}' does not exist."}, status=404)


# Get articles from a given Category
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_category_news(request, title: str):
    try:

        # Get Category by given title & articles under it
        category = Category.objects.get(title=title)
        articles = Article.objects.filter(category=category)

        # Return under DRF serialization by page
        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    # Return a bad response ( 404 ) if the Category does not exist
    except Category.DoesNotExist:
        return Response({"error": f"Category '{title}' does not exist."}, status=404)


# Get articles from a given Tag
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_tagged_news(request, title: str):
    try:

        # Get Tag by given title & articles under it
        tag = Tag.objects.get(title=title)
        articles = Article.objects.filter(tags=tag)

        # Return under DRF serialization by page
        paginator = CustomPagination()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    # Return a bad response ( 404 ) if the Tag does not exist
    except Tag.DoesNotExist:
        return Response({"error": f"Tag '{title}' does not exist."}, status=404)


# Add given article to the user's favorite list
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_article(request, articleId):
    try:

        # Get article by the given id
        article = Article.objects.get(id=articleId)

        # Get the current User
        user = request.user

        # Add favorite relationship
        article.favorite(user)
        return Response({"message": f"User - {user.username} favorited article with id - {articleId}."})

    # Return a bad response ( 404 ) if the Article does not exist
    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


# Remove given article from the user's favorite list
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfavorite_article(request, articleId):
    try:

        # Get article by the given id
        article = Article.objects.get(id=articleId)

        # Get the current User
        user = request.user

        # Remove favorite relationship
        article.unfavorite(user)
        return Response({"message": f"User - {user.username} unfavorited article with id - {articleId}."})

    # Return a bad response ( 404 ) if the Article does not exist
    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


# Add given article to the user's read later list
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def readlater_article(request, articleId):
    try:

        # Get article by the given id
        article = Article.objects.get(id=articleId)

        # Get the current User
        user = request.user

        # Add read later relationship
        article.read_later(user)
        return Response({"message": f"User - {user.username} read later article with id - {articleId}."})

    # Return a bad response ( 404 ) if the Article does not exist
    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


# Remove given article from the user's read later list
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unreadlater_article(request, articleId):
    try:

        # Get article by the given id
        article = Article.objects.get(id=articleId)

        # Get the current User
        user = request.user

        # Remove read later relationship
        article.unread_later(user)
        return Response({"message": f"User - {user.username} unread later article with id - {articleId}."})

    # Return a bad response ( 404 ) if the Article does not exist
    except Article.DoesNotExist:
        return Response({"error": f"Article with id - '{articleId}' does not exist."}, status=404)


###################################
# RECOMMENDATION SYSTEM ENDPOINTS #
###################################
# Collaborative Filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_articles_by_users(request):

    # Get the current User
    user = request.user

    # Find articles favorited by users who have also favorited articles that this user has favorited
    favorited_articles_ids = user.favorite_articles.values_list('id', flat=True)
    similar_users = User.objects.filter(favorite_articles__in=favorited_articles_ids).exclude(id=user.id).distinct()
    recommended_articles = Article.objects.filter(favorited_by__in=similar_users).exclude(favorited_by=user)

    # Return under DRF serialization by page
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(recommended_articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


# Content Filtering
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_articles_by_content(request):

    # Get the current User
    user = request.user

    # Get categories and tags of articles favorited by the user
    favorited_categories = user.favorite_articles.values_list('category__id', flat=True).distinct()
    favorited_tags = user.favorite_articles.values_list('tags__id', flat=True).distinct()

    # Filter articles based on favorited categories or favorited tags, and exclude those already favorited by the user
    recommended_articles = Article.objects.filter(
        Q(category__id__in=favorited_categories) | Q(tags__id__in=favorited_tags)
    ).exclude(favorited_by=user).distinct()

    # Return under DRF serialization by page
    paginator = CustomPagination()
    paginated_articles = paginator.paginate_queryset(recommended_articles, request)
    serializer = ArticleSerializer(paginated_articles, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


############################
# AUTHENTICATION ENDPOINTS #
############################
# Register new user
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    # Get the form data from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # In case of complete data
    if username and password:

        # Check if user with given credentials ( username ) already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Else add a new user & assign a token
        # Django authentication handles password hashing !!
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    # Return a Bad Response - Incomplete Data
    else:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


# Login old user
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):

    # Get the form data from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # Get the user with the given credentials
    # Django authentication handles password hashing !!
    user = authenticate(username=username, password=password)

    # If the user does exist get / assign a token to it
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    # Else, return a Bad Response - User does not exist
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Logout current user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    # Logout the current user
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
