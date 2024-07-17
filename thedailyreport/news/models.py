###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


#####################
# MODEL DEFINITIONS #
#####################

class User(AbstractUser):
    """
    User Objects inherit all attributes of AbstractUser
    Implements more user characteristic fields:
    - date of birth
    - address
    - phone number
    - gender
    - biography
    - social media links
    Adds a follow method to a News Source
    """

    # User Characteristic Information
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    biography = models.TextField(blank=True)
    social_media_links = models.CharField(max_length=255, blank=True)

    # Users can follow NewsSources
    followed_news_sources = models.ManyToManyField('NewsSource', related_name='followers')

    # User - NewsSource Interactions
    def follow(self, news_source):
        self.followed_news_sources.add(news_source)

    def unfollow(self, news_source):
        self.followed_news_sources.remove(news_source)

    def is_following(self, news_source):
        return self.followed_news_sources.filter(id=news_source.id).exists()


# Media Class
class Media(models.Model):
    """
    Media Objects are defined by their respective URL
    """

    # TODO: Improvement => Save Medias to Database ( for persistence )
    url = models.URLField(max_length=1024)

    # String Format: URL of the Media
    def __str__(self):
        return self.url


# Category Class
class Category(models.Model):
    """
    Category Objects are defined by their titles
    """

    title = models.CharField(max_length=64)

    # String Format: Title of the Category
    def __str__(self):
        return self.title


# Tag Class
class Tag(models.Model):
    """
    Tag Objects are defined by their titles
    """

    title = models.CharField(max_length=64)

    # String Format: Title of the Tag
    def __str__(self):
        return self.title


# News Source Class
# Admin Moderated
class NewsSource(models.Model):
    """
    NewsSource Objects are defined by the following fields:
    - name
    - city
    - address
    - phone number
    - e-mail address
    - ( TBA ) Political Bias
    """

    # Basic Contact Information about the News Source
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=10)
    email_address = models.EmailField()

    # Advanced Information about the News Source
    # Political bias - from -100 (extreme-left) to 100 (extreme-right)
    political_bias = models.IntegerField(default=0, validators=[MinValueValidator(-100), MaxValueValidator(100)])

    # String Format: Name of the News Source
    def __str__(self):
        return self.name


# Article Class
class Article(models.Model):
    """
    Article Objects are defined by the following fields
    - title
    - summary ( provided & TBA AI generated )
    - content
    - preview media ( image )
    - writer

    They are accompanied by metadata:
    - publish date
    - last updated date
    - source url
    - publisher
    - tags
    - category

    Users can interact with articles:
    - like
    - favorite
    - read later

    For faster query times the article's most important information: title, content, media are hashed
    The hashes are checked against each other to determine 'equality' ( ~being the same article )
    """

    # Article Query Data
    title_hash = models.CharField(max_length=64)
    content_hash = models.CharField(max_length=64)
    media_hash = models.CharField(max_length=64, blank=True, null=True)

    # Article Information
    title = models.CharField(max_length=1024)
    provided_summary = models.TextField(max_length=2048)
    generated_summary = models.TextField(max_length=2048)
    content = models.TextField(max_length=5096)
    media_preview = models.ForeignKey(to=Media, on_delete=models.PROTECT, related_name="preview_media")
    writer = models.CharField(max_length=128)

    # Article Metadata
    publish_date = models.CharField(max_length=64)
    last_updated_date = models.CharField(max_length=64)
    url = models.URLField(max_length=1024)
    publisher = models.ForeignKey(to=NewsSource, on_delete=models.CASCADE, related_name="articles")
    tags = models.ManyToManyField(to=Tag, related_name="tagged_articles")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="categorized_articles")

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

    # String Format: Title of the Article
    def __str__(self):
        return self.title

