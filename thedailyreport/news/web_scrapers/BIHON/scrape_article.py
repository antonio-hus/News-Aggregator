# Imports Section
# Python Libraries
import requests
from bs4 import BeautifulSoup


# Get article information from the given URL
def get(url):
    article_data = {}

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        article = BeautifulSoup(response.content, 'html.parser')

        # Finding main content
        paragraphs = article.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]
        content = '\n'.join(article_content) if article_content else "Content not found."

        # Finding the author's name
        author = article.find('div', class_='author').find('i')
        if author:
            author_name = author.text.strip()
        else:
            author_name = "No writer mentioned"

        # Finding the image's url
        image_url = article.find('div', class_='tac default').find('img')['src']

        article_data = {
            "writer": author_name,
            "publish_date": '',
            "last_updated_date": '',
            "tags": ["N/A"],
            "content": content,
            "image": image_url
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing article: {e}")

    return article_data
