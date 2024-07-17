# Imports Section
# Python Libraries
import requests
from bs4 import BeautifulSoup


# Gets article information from ProTV Website
def get(url):
    article_data = {
        "writer": '',
        "tags": [],
        "content": '',
        "category": '',
        "image": '',
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content of the page
        article = BeautifulSoup(response.content, 'html.parser')

        # Extracting media
        image_div = article.find('div', class_='article--media')
        if image_div:
            image = image_div.find('img')['src'] \
                if image_div.find('img') else "No Media Found"

        # Finding main content
        content_div = article.find('div', class_='article--text')
        paragraphs = content_div.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]
        content = '\n'.join(article_content[:-4]) if article_content else "Content not found."

        # Extracting Author
        author = article.find('div', class_="author--name").find('a')
        if author:
            author_name = author.text.strip()
        else:
            author_name = "No writer mentioned"

        # Extracting Category
        category = article.find('div', class_="article--section-information").find('a')
        if category:
            category_title = category.text.strip()
        else:
            category_title = "N/A"

        # Extracting tags
        tags = [tag.get_text().strip() for tag in article.find_all('a', class_="article__info__tags_a")]

        article_data = {
            "writer": author_name,
            "tags": tags,
            "content": content,
            "category": category_title,
            "image": image,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing article: {e}")

    return article_data
