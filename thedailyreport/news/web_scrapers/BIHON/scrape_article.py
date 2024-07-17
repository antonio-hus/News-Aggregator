###################
# IMPORTS SECTION #
###################
# Python Libraries
import requests
from bs4 import BeautifulSoup


########################
# NEWS ARTICLE SCRAPER #
########################
def get(url):

    # Return value if scraping goes wrong
    article_data = {
        "writer": 'No writer mentioned',
        "tags": ["N/A"],
        "content": 'No content found',
        "image": 'No image found'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        article = BeautifulSoup(response.content, 'html.parser')

        # Extracting main content
        paragraphs = article.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]
        content = '\n'.join(article_content) if article_content else "No content found"

        # Extracting the writer's name
        writer = article.find('div', class_='author').find('i')
        if writer:
            writer_name = writer.text.strip()
        else:
            writer_name = "No writer mentioned"

        # Extract media preview
        image_url = article.find('div', class_='tac default').find('img')['src']

        # Set article data
        article_data = {
            "writer": writer_name,
            "tags": ["N/A"],
            "content": content,
            "image": image_url
        }

    # Catch exceptions
    except Exception:
        pass

    # Returns above defined default values if something goes wrong with scraping
    # Returns the actual values if everything goes well
    return article_data
