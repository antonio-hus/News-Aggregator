# Imports Section
import requests
from bs4 import BeautifulSoup

# Web Scraper


# Gets news from dig24 Website
def get():

    # Create News List
    article_list = []

    # Send a GET request to the URL
    response = requests.get("https://www.digi24.ro/")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the news article elements
        articles = soup.find_all('article', class_='article article-alt')

        # Loop through each article and extract relevant information
        for article in articles:

            # Extract title
            title_elem = article.find('h3', class_='article-title')
            title = title_elem.get_text().strip() if title_elem else "No title found"

            # Extract summary
            summary_elem = article.find('p', class_='article-intro')
            summary = summary_elem.get_text().strip() if summary_elem else "No summary found"

            # Extract URL
            url_elem = article.find('a')['href'] if article.find('a') else "No URL found"
            if url_elem[0] == '/':
                url_elem = "https://www.digi24.ro" + url_elem

            # Extract image source
            img_elem = article.find('img')['src'] if article.find('img') else "No image found"

            # Create a dictionary to store the extracted data for this article
            article_data = {
                'url': url_elem,
                'img_src': img_elem,
                'title': title,
                'summary': summary,
            }

            # Append the dictionary to the articles_list
            article_list.append(article_data)

    return article_list
