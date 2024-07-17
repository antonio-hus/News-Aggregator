# Imports Section
# Python Libraries
import requests
from bs4 import BeautifulSoup


# Gets article information from ZF Website
def get(url):

    article_data = {
        "writer": 'No writer mentioned',
        "tags": ["N/A"],
        "content": 'No content found',
        "category": 'No category found',
        "summary": 'No summary found',
        "image": 'No image found'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('div', class_='article')
        if not article:
            return article_data

        category_div = article.find('span', class_='underline')
        if category_div:
            category = category_div.find('span', class_='labelTag fleft').text.strip()
        else:
            category = 'N/A'

        # Finding main content
        paragraphs = article.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]

        summary = article_content[1]
        if 'Autor' in summary:
            summary = article_content[2]
            content = '\n'.join(article_content[2:-19]) if article_content else "Content not found."
        else:
            content = '\n'.join(article_content[1:-19]) if article_content else "Content not found."

        image = article.find('img')['src']
        image = 'https:' + image

        author_div = article.find('div', class_='author clear').find('a')
        if author_div:
            author_name = author_div.text.strip()
        else:
            author_name = "No writer mentioned"

        article_data = {
            "writer": author_name,
            "tags": ["N/A"],
            "content": content,
            "category": category,
            "summary": summary,
            "image": image
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing article: {e}")

    return article_data
