###################
# IMPORTS SECTION #
###################
# Django Rest-Framework (DRF) Libraries
from rest_framework import serializers
# Project Libraries
from .models import User, Media, NewsSource, Tag, Category, Article


##########################
# SERIALIZERS DEFINITION #
##########################
# User Class Serializer ( Basic Information )
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'followed_news_sources')


# User Class Serializer ( Extended Information )
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth',
                  'address', 'phone_number', 'gender',
                  'biography', 'social_media_links', 'date_joined', 'last_login']
        read_only_fields = ['username', 'email', 'date_joined', 'last_login']


# Media Class Serializer
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'url')


# Category Class Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


# Tag Class Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


# News Source Serializer
class NewsSourceSerializer(serializers.ModelSerializer):

    # Additional Information
    # Boolean - Does the current user follow the given news source
    is_followed_by_user = serializers.SerializerMethodField()

    class Meta:
        model = NewsSource
        fields = ['id', 'name', 'city', 'address', 'phone_number', 'email_address', 'political_bias',
                  'is_followed_by_user']

    # Determines if the current user follows the given news source
    def get_is_followed_by_user(self, obj):

        # Get the request from the context of the serializer
        request = self.context.get('request', None)

        # Return True if the user is following the News Source
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)

        # Return False otherwise
        return False


# Article Class Serializer
class ArticleSerializer(serializers.ModelSerializer):

    # Serialize Custom Classes
    media_preview = MediaSerializer()
    publisher = NewsSourceSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    # Additional Information
    is_favorited = serializers.SerializerMethodField()
    is_read_later = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id', 'title_hash', 'content_hash', 'media_hash', 'publish_date', 'last_updated_date',
            'url', 'publisher', 'tags', 'category', 'title', 'provided_summary', 'generated_summary',
            'content', 'media_preview', 'writer', 'liked_by', 'favorited_by', 'read_later_by',
            'is_favorited', 'is_read_later'
        )

    # Gets the representation of the Article
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_by'] = UserSerializer(instance.liked_by.all(), many=True).data
        representation['favorited_by'] = UserSerializer(instance.favorited_by.all(), many=True).data
        representation['read_later_by'] = UserSerializer(instance.read_later_by.all(), many=True).data
        return representation

    # Determines if the current user has the article instance in favorite
    def get_is_favorited(self, instance):

        # Get the request from the context of the serializer
        request = self.context.get('request')

        # Return True if the user is following the News Source
        if request and request.user.is_authenticated:
            return instance.favorited_by.filter(id=request.user.id).exists()

        # Return False otherwise
        return False

    # Determines if the current user has the article instance in read later
    def get_is_read_later(self, instance):

        # Get the request from the context of the serializer
        request = self.context.get('request')

        # Return True if the user is following the News Source
        if request and request.user.is_authenticated:
            return instance.read_later_by.filter(id=request.user.id).exists()

        # Return False otherwise
        return False
