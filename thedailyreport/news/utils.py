###################
# IMPORTS SECTION #
###################
# Python Libraries
import requests
import os
from datetime import datetime, timedelta
import logging
# Django Libraries
from django.utils import timezone
from django.db import transaction
# User Defined
from .web_scrapers import DIGI24, BIHON, HOTNEWS, PROTV, ZIARULDECLUJ
from .models import Media, Category, Tag, NewsSource, Article

###################
# LOGGING ACTIONS #
###################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('periodic_update.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


###########################
# WEB SCRAPERS OPERATIONS #
###########################

# Fetch Articles using Web Scrapers
def getArticles():
    """
    Functionality:
    - fetch articles from all sources
    """

    article_list = []
    article_list.append(DIGI24.scrape_news.get())
    article_list.append(BIHON.scrape_news.get())

    return article_list


#######################
# DATABASE OPERATIONS #
#######################


# Create or get Useful Objects
def create_or_get_category(title):
    category, created = Category.objects.get_or_create(title=title)
    return category


def create_or_get_tag(title):
    """
    Creates new Tag(s) or retrieves existing one(s) by title.
    """
    tag, created = Tag.objects.get_or_create(title=title)
    return tag


def create_or_get_media(url):
    media, created = Media.objects.get_or_create(url=url)
    return media


def create_or_get_publisher(name):
    media, created = NewsSource.objects.get_or_create(name=name)
    return media


# Periodic Update of Articles in DataBase
# To be called every 8 hours ( at usual down-times )
@transaction.atomic
def periodicUpdate():
    """
    Functionality:
    - add in database new articles
    - update in database modified articles
    - delete articles older than 7 days
    """
    article_list = getArticles()
    logger.debug(f"Received article list: {article_list}")

    for publisher in article_list:
        for article in publisher:
            logger.debug(f"Processing article: {article}")

            article["publisher"] = create_or_get_publisher(article["publisher"])
            if article["publish_date"] == "":
                article["publish_date"] = timezone.now()
            if article["last_updated_date"] == "":
                article["last_updated_date"] = timezone.now()

            # Object is already in database, and nothing changed
            if Article.objects.filter(title_hash=article["title_hash"],
                                      content_hash=article["content_hash"],
                                      media_hash=article["media_hash"]).exists():

                logger.debug("Article already exists in database, no changes detected.")
                # Delete articles older than 7 days
                seven_days_ago = timezone.now() - timedelta(days=7)
                deleted_count, _ = Article.objects.filter(publish_date__lt=seven_days_ago).delete()
                logger.debug(f"Deleted {deleted_count} articles older than 7 days.")
                continue

            # Object is already in database, but something changed
            # Media Preview Changed
            elif Article.objects.filter(title_hash=article["title_hash"],
                                        content_hash=article["content_hash"]).exists():

                logger.debug("Found existing article with changed media preview.")
                # Get the object
                found_article = Article.objects.get(title_hash=article["title_hash"],
                                                    content_hash=article["content_hash"])

                # Update Media & Media Hash
                found_article.media_hash = article["media_hash"]
                found_article.media_preview = create_or_get_media(article["media_preview"])
                found_article.last_updated_date = timezone.now()
                found_article.save()
                logger.debug("Updated existing article.")
                continue

            # Content Changed
            elif Article.objects.filter(title_hash=article["title_hash"],
                                        media_hash=article["media_hash"]).exists():
                logger.debug("Found existing article with changed content.")
                # Get the object
                found_article = Article.objects.get(title_hash=article["title_hash"],
                                                    media_hash=article["media_hash"])

                # Update Media & Media Hash
                found_article.content_hash = article["content_hash"]
                found_article.content = article["content"]
                found_article.last_updated_date = timezone.now()
                found_article.save()
                logger.debug("Updated existing article.")
                continue

            # Title Changed
            elif Article.objects.filter(content_hash=article["content_hash"],
                                        media_hash=article["media_hash"]).exists():

                logger.debug("Found existing article with changed title.")
                # Get the object
                found_article = Article.objects.get(content_hash=article["content_hash"],
                                                    media_hash=article["media_hash"])
                found_article.title_hash = article["title_hash"]
                found_article.title = article["title"]
                found_article.last_updated_date = timezone.now()
                found_article.save()
                logger.debug("Updated existing article.")
                continue

            # Object was not found in the database => new Article
            else:
                logger.debug("Creating new article in database.")
                new_article = Article(
                    title_hash=article["title_hash"],
                    content_hash=article["content_hash"],
                    media_hash=article["media_hash"],
                    publish_date=article["publish_date"],
                    last_updated_date=article["last_updated_date"],
                    publisher=article["publisher"],
                    url=article["url"],
                    writer=article["writer"],
                    title=article["title"],
                    provided_summary=article["provided_summary"],
                    generated_summary="",  # TODO: AI COMPLETION HERE
                    media_preview=create_or_get_media(article["media_preview"]),
                    content=article["content"],
                    category=create_or_get_category(article["category"])
                )
                new_article.save()

                # Add tags
                for tag_title in article["tags"]:
                    tag = create_or_get_tag(tag_title)
                    new_article.tags.add(tag)

                new_article.save()
                logger.debug("New article created.")


####################
# MEDIA OPERATIONS #
####################


def checkMediaURL(url: str) -> bool:
    """
    Checks if a Media's URL is still valid
    Returns True if it is valid
    Returns False if it is invalid
    """
    try:
        # Getting the response of the URL
        response = requests.head(url, allow_redirects=True)

        # Check if the status code is in the range of 200-399 ( Valid URL )
        if 200 <= response.status_code < 400:
            return True
        else:
            return False

    # Invalid Request => Invalid Media
    except requests.RequestException:
        return False


def getMediaURL(url: str) -> str:
    """
    Returns the URL of the Media Item if URL valid
    Returns the URL of a placeholder if URL not valid
    """
    placeholder_url = "https://example.com/placeholder.jpg"

    # Valid Media URL
    if checkMediaURL(url):
        return url

    # PlaceHolder URL
    return placeholder_url


def downloadFile(url: str, dest_folder: str):
    """
    Downloads a file from a URL and saves it to a destination folder
    Returns the file path of the downloaded file
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Extract file name from URL and create full path
        filename = os.path.join(dest_folder, os.path.basename(url))

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return filename
    except requests.RequestException:
        return None


def getMediaFile(url: str):
    """
    Returns the File of the Media Item if URL valid
    Returns the File of a placeholder if URL not valid
    """
    placeholder_file = "../media/media_placeholder.png"

    # Valid Media URL
    if checkMediaURL(url):
        file_path = downloadFile(url, "../media")
        if file_path:
            return file_path

    # PlaceHolder File
    return placeholder_file
