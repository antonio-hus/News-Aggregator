###################
# IMPORTS SECTION #
###################
# Python Libraries
import requests
import hashlib
from bs4 import BeautifulSoup
# Project Libraries
from . import scrape_article


#####################
# NEWS LIST SCRAPER #
#####################
def get():

    # Create News List
    article_list = []

    # Send a GET request to the URL
    response = requests.get("https://www.digi24.ro/")
    if response.status_code == 200:

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news article elements
        articles = soup.find_all('article', class_='article article-alt')

        # Loop through each article and extract relevant information
        for article in articles:

            # Set Publisher
            publisher = "Digi24"

            # Extract title
            title_elem = article.find('h3', class_='article-title')
            title = title_elem.get_text().strip() if title_elem else "No title found"

            # Extract summary
            summary_elem = article.find('p', class_='article-intro')
            summary = summary_elem.get_text().strip() if summary_elem else "No summary found"

            # Extract category
            category_elem = article.find('a', class_='article-tag')
            category = category_elem.get_text().strip() if category_elem else "No category found"

            # Extract URL
            url = article.find('a')['href'] if article.find('a') else "No URL found"
            if url[0] == '/':
                url = "https://www.digi24.ro" + url

            if "digisport.ro" in url:
                continue

            # Extract image source
            img_elem = article.find('img')['src'] if article.find('img') else "No image found"

            # Create a dictionary to store the extracted data for this article
            article_data = scrape_article.get(url)
            complete_article_data = {
                "title_hash": hashlib.sha256(title.encode('utf-8')).hexdigest(),
                "content_hash": hashlib.sha256(article_data["content"].encode('utf-8')).hexdigest(),
                "media_hash": hashlib.sha256(img_elem.encode('utf-8')).hexdigest(),
                "publisher": publisher,
                "url": url,
                "writer": article_data["writer"],
                "publish_date": '',
                "last_updated_date": '',
                "category": category,
                "tags": article_data["tags"],
                "title": title,
                "provided_summary": summary,
                "media_preview": img_elem,
                "content": article_data["content"]
            }

            # Append the dictionary to the articles_list
            article_list.append(complete_article_data)

    # Returns the list of articles if everything went well
    # Returns an empty list in case of errors
    return article_list
