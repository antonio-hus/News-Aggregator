# Imports Section
# Python Libraries
import requests
import hashlib
from bs4 import BeautifulSoup
from . import scrape_article


# Gets news from ZF Website
def get():

    # Create News List
    article_list = []

    # Send a GET request to the URL
    response = requests.get("https://www.zf.ro/zf-24/")
    if response.status_code == 200:

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news article elements
        articles = soup.find_all('div', class_='flux news clear')

        # Loop through each article and extract relevant information
        for article in articles:

            # Set Publisher
            publisher = "Ziarul Financiar"

            # Extract title
            title_elem = article.find('h2')
            title = title_elem.get_text().strip() if title_elem else "No title found"

            # Extract URL
            url_a = article.find('a')
            url_elem = url_a['href'] if article.find('a') else "No URL found"
            url_elem = "https://www.zf.ro" + url_elem

            # Extract image source
            img_elem = url_a.find('img') if url_a else None
            if img_elem:
                img_src = img_elem.get('data-src', img_elem.get('src', "No image found"))
                img_src = 'https:' + img_src if img_src.startswith('//') else img_src
            else:
                img_src = "No image found"

            # Create a dictionary to store the extracted data for this article
            article_data = scrape_article.get(url_elem)
            complete_article_data = {
                "title_hash": hashlib.sha256(title.encode('utf-8')).hexdigest(),
                "content_hash": hashlib.sha256(article_data["content"].encode('utf-8')).hexdigest(),
                "media_hash": hashlib.sha256(img_src.encode('utf-8')).hexdigest(),
                "publisher": publisher,
                "url": url_elem,
                "writer": article_data["writer"],
                "publish_date": '',
                "last_updated_date": '',
                "category": article_data["category"],
                "tags": article_data["tags"],
                "title": title,
                "provided_summary": article_data["summary"],
                "media_preview": img_src,
                "content": article_data["content"]
            }

            # Append the dictionary to the articles_list
            article_list.append(complete_article_data)

    return article_list
