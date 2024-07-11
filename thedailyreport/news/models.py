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


# Image Class
class Image(models.Model):

    # Image Defined by its URL
    # TODO: Improvement => Save Images to Database ( for persistence )
    url = models.URLField()

    def __str__(self):
        return self.url


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
    image_hash = models.CharField(max_length=64, blank=True, null=True)
    publish_date = models.DateTimeField()
    last_updated_date = models.DateTimeField()

    # Article Information Data
    writer = models.CharField(max_length=128)
    tags = models.CharField(max_length=256, blank=True, null=True)

    # Article Preview Information
    title_preview = models.CharField(max_length=256)
    content_preview = models.TextField()
    image_preview = models.ForeignKey(to=Image, on_delete=models.PROTECT, related_name="preview_image")

    # Article Content Information
    title_full = models.CharField(max_length=256)
    content_full = models.TextField()
    images_full = models.ManyToManyField(to=Image, related_name="full_images")

    # Article Mailing Information
    title_mailing = models.CharField(max_length=256)
    content_mailing = models.TextField()
    images_mailing = models.ManyToManyField(to=Image, related_name="mailing_images")

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
