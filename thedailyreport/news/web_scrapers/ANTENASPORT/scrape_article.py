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
        "summary": 'No summary found',
        "image": 'No image found'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content of the page
        article = BeautifulSoup(response.content, 'html.parser')

        # Finding main content
        article_content = []
        paragraph_sections = article.find('div', class_='new-design-article-content')
        paragraphs = paragraph_sections.find_all('p')
        for paragraph in paragraphs:
            article_content.append(paragraph.text.strip())

        content = ""
        for article_piece in article_content[2:-2]:
            if "Reclamă" in article_piece:
                continue
            elif article_piece in content:
                continue
            else:
                content += article_piece
                content += '\n'
        summary = article_content[0]

        image_div = article.find('div', class_='new-design-article-content')
        image = image_div.find('img')['src']

        author_div = article.find('section', class_='article-hero').find('a')
        if author_div:
            author_name = author_div.text.strip()
        else:
            author_name = "No writer mentioned"

        if author_name == 'Home':
            author_name = "No writer mentioned"

        article_data = {
            "writer": author_name,
            "tags": ["N/A"],
            "content": content,
            "summary": summary,
            "image": image
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing article: {e}")

    return article_data
