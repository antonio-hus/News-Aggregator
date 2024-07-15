from rest_framework import serializers
from .models import User, Media, NewsSource, Tag, Category, Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'followed_news_sources')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_of_birth',
                  'address', 'phone_number', 'gender',
                  'biography', 'social_media_links', 'date_joined', 'last_login']
        read_only_fields = ['username', 'email', 'date_joined', 'last_login']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'url')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class NewsSourceSerializer(serializers.ModelSerializer):
    is_followed_by_user = serializers.SerializerMethodField()

    class Meta:
        model = NewsSource
        fields = ['id', 'name', 'city', 'address', 'phone_number', 'email_address', 'political_bias',
                  'is_followed_by_user']

    def get_is_followed_by_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class ArticleSerializer(serializers.ModelSerializer):
    media_preview = MediaSerializer()
    publisher = NewsSourceSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_by'] = UserSerializer(instance.liked_by.all(), many=True).data
        representation['favorited_by'] = UserSerializer(instance.favorited_by.all(), many=True).data
        representation['read_later_by'] = UserSerializer(instance.read_later_by.all(), many=True).data
        return representation

    def get_is_favorited(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return instance.favorited_by.filter(id=request.user.id).exists()
        return False

    def get_is_read_later(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return instance.read_later_by.filter(id=request.user.id).exists()
        return False
