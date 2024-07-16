# Imports Section
# Python Libraries
import requests
import hashlib
from bs4 import BeautifulSoup
from . import scrape_article


# Gets news from ProTV Website
def get():

    # Create News List
    article_list = []

    # Send a GET request to the URL
    response = requests.get("https://stirileprotv.ro/ultimele-stiri/")
    if response.status_code == 200:

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news article elements
        articles = soup.find_all('article', class_='grid article')

        # Loop through each article and extract relevant information
        for article in articles:

            # Set Publisher
            publisher = "ProTV"

            # Extract title
            title_elem = article.find('div', class_='article-title').find('h2')
            title = title_elem.get_text().strip() if title_elem else "No title found"

            # Extract summary
            summary_elem = article.find('div', class_='article-lead')
            summary = summary_elem.get_text().strip() if summary_elem else "No summary found"

            # Extract URL
            url_elem = article.find('div', class_='article-title').find('a')['href'] if (
                article.find('div', class_='article-title').find('a')) else "No URL found"

            # Create a dictionary to store the extracted data for this article
            article_data = scrape_article.get(url_elem)
            complete_article_data = {
                "title_hash": hashlib.sha256(title.encode('utf-8')).hexdigest(),
                "content_hash": hashlib.sha256(article_data["content"].encode('utf-8')).hexdigest(),
                "media_hash": hashlib.sha256(article_data["image"].encode('utf-8')).hexdigest(),
                "publisher": publisher,
                "url": url_elem,
                "writer": article_data["writer"],
                "publish_date": '',
                "last_updated_date": '',
                "category": article_data["category"],
                "tags": article_data["tags"],
                "title": title,
                "provided_summary": summary,
                "media_preview": article_data["image"],
                "content": article_data["content"]
            }

            # Append the dictionary to the articles_list
            article_list.append(complete_article_data)

    return article_list
