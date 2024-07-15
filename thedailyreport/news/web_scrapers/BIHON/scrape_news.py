# Imports Section
# Python Libraries
import requests
import hashlib
from bs4 import BeautifulSoup
from . import scrape_article


# Gets news from Bihoreanul Website
def get():

    # Create News List
    article_list = []

    # Send a GET request to the URL
    response = requests.get("https://www.ebihoreanul.ro/")
    if response.status_code == 200:

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news article elements
        articles = soup.find_all('div', class_='article')

        # Loop through each article and extract relevant information
        for article in articles:

            # Set Publisher
            publisher = "Bihoreanul"

            # Extract title & URL Element
            title_element = article.find('div', class_='title').find('a')
            title = title_element.text.strip()
            link = title_element['href']

            # Extract summary text
            summary = article.find('div', class_='text').text.strip()

            # Extract category dynamically
            category = None
            div_elements = article.find('div', class_='article-content').find_all('div')
            for div in div_elements:
                if div.text.strip() and div != div.find('div', class_='img') and div != div.find('div',
                                                                                                   class_='text'):
                    category = div.text.strip()
                    break

            # Extract image URL
            image_url = article.find('div', class_='img').find('img')['src']

            # Create a dictionary to store the extracted data for this article
            article_data = scrape_article.get(link)
            complete_article_data = {
                "title_hash": hashlib.sha256(title.encode('utf-8')).hexdigest(),
                "content_hash": hashlib.sha256(article_data["content"].encode('utf-8')).hexdigest(),
                "media_hash": hashlib.sha256(image_url.encode('utf-8')).hexdigest(),
                "publisher": publisher,
                "url": link,
                "writer": article_data["writer"],
                "publish_date": article_data["publish_date"],
                "last_updated_date": article_data["last_updated_date"],
                "category": category,
                "tags": article_data["tags"],
                "title": title,
                "provided_summary": summary,
                "media_preview": image_url,
                "content": article_data["content"]
            }

            # Append the dictionary to the articles_list
            article_list.append(complete_article_data)

    return article_list
