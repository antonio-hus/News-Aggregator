# Imports Section
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# User Class
class User(AbstractUser):
    """
    Inherits all attributes of AbstractUser
    Adds a follow method to a News Source
    """

    followed_news_sources = models.ManyToManyField('NewsSource', related_name='followers')

    def follow(self, news_source):
        self.followed_news_sources.add(news_source)

    def unfollow(self, news_source):
        self.followed_news_sources.remove(news_source)

    def is_following(self, news_source):
        return self.followed_news_sources.filter(id=news_source.id).exists()


# Media Class
class Media(models.Model):

    # Media Defined by its URL
    # TODO: Improvement => Save Medias to Database ( for persistence )
    url = models.URLField(max_length=1024)

    def __str__(self):
        return self.url


# Category Class
class Category(models.Model):

    # Category is defined by its title
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


# Tag Class
class Tag(models.Model):

    # Tag is defined by its name
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


# News Source Class
# Admin Moderated
class NewsSource(models.Model):

    # Basic Contact Information about the News Source
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=10)
    email_address = models.EmailField()

    # Advanced Information about the News Source
    # Political bias - from -100 (extreme-left) to 100 (extreme-right)
    political_bias = models.IntegerField(default=0, validators=[MinValueValidator(-100), MaxValueValidator(100)])

    def __str__(self):
        return self.name


# Article Class
class Article(models.Model):

    # Header Data
    title_hash = models.CharField(max_length=64)
    content_hash = models.CharField(max_length=64)
    media_hash = models.CharField(max_length=64, blank=True, null=True)
    publish_date = models.CharField(max_length=64)
    last_updated_date = models.CharField(max_length=64)
    url = models.URLField()
    publisher = models.ForeignKey(to=NewsSource, on_delete=models.CASCADE, related_name="articles")
    tags = models.ManyToManyField(to=Tag, related_name="tagged_articles")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="categorized_articles")

    # Article Information
    title = models.CharField(max_length=256)
    provided_summary = models.TextField()
    generated_summary = models.TextField()
    content = models.TextField()
    media_preview = models.ForeignKey(to=Media, on_delete=models.PROTECT, related_name="preview_media")
    writer = models.CharField(max_length=128)

    # User Interactions
    liked_by = models.ManyToManyField(User, related_name='liked_articles', blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_articles', blank=True)
    read_later_by = models.ManyToManyField(User, related_name='read_later_articles', blank=True)

    def like(self, user):
        self.liked_by.add(user)

    def unlike(self, user):
        self.liked_by.remove(user)

    def likes_count(self):
        return self.liked_by.count()

    def favorite(self, user):
        self.favorited_by.add(user)

    def unfavorite(self, user):
        self.favorited_by.remove(user)

    def favorite_count(self):
        return self.favorited_by.count()

    def read_later(self, user):
        self.read_later_by.add(user)

    def unread_later(self, user):
        self.read_later_by.remove(user)

    def __str__(self):
        return self.title

