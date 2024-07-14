from rest_framework import serializers
from .models import User, Media, NewsSource, Tag, Category, Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'followed_news_sources')


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
    class Meta:
        model = NewsSource
        fields = ('id', 'name', 'city', 'address', 'phone_number', 'email_address', 'political_bias')


class ArticleSerializer(serializers.ModelSerializer):
    media_preview = MediaSerializer()
    publisher = NewsSourceSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = (
            'id', 'title_hash', 'content_hash', 'media_hash', 'publish_date', 'last_updated_date',
            'url', 'publisher', 'tags', 'category', 'title', 'provided_summary', 'generated_summary',
            'content', 'media_preview', 'writer', 'liked_by', 'favorited_by', 'read_later_by'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_by'] = UserSerializer(instance.liked_by.all(), many=True).data
        representation['favorited_by'] = UserSerializer(instance.favorited_by.all(), many=True).data
        representation['read_later_by'] = UserSerializer(instance.read_later_by.all(), many=True).data
        return representation
