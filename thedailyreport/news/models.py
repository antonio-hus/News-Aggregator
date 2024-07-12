# Imports Section
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


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
    url = models.URLField()

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

    # Tag is defined by its name and category
    title = models.CharField(max_length=64)
    categories = models.ManyToManyField(to=Category, related_name="categorized_tags")

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
    publish_date = models.DateTimeField()
    last_updated_date = models.DateTimeField()

    # Article Information Data
    writer = models.CharField(max_length=128)
    tags = models.ManyToManyField(to=Tag, related_name="tagged_articles")
    categories = models.ManyToManyField(to=Category, related_name="categorized_articles")

    # Article Preview Information
    title_preview = models.CharField(max_length=256)
    content_preview = models.TextField()
    media_preview = models.ForeignKey(to=Media, on_delete=models.PROTECT, related_name="preview_media")

    # Article Content Information
    title_full = models.CharField(max_length=256)
    content_full = models.TextField()
    medias_full = models.ManyToManyField(to=Media, related_name="full_medias")

    # Article Mailing Information
    title_mailing = models.CharField(max_length=256)
    content_mailing = models.TextField()
    medias_mailing = models.ManyToManyField(to=Media, related_name="mailing_medias")

    # News Source owner of article
    publisher = models.ForeignKey(to=NewsSource, on_delete=models.CASCADE, related_name="articles")

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
        return self.title_preview
