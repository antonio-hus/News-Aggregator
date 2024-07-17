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
        "summary": 'No summary found',
        "image": 'No image found'
    }

    try:
        
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content of the page
        article = BeautifulSoup(response.content, 'html.parser')

        # Extracting main content
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

        # Extracting article headline
        summary = article_content[0]

        # Extracting media preview
        image_div = article.find('div', class_='new-design-article-content')
        image = image_div.find('img')['src']

        # Extracting writer
        writer_div = article.find('section', class_='article-hero').find('a')
        if writer_div and writer_div != "Home":
            writer_name = writer_div.text.strip()
        else:
            writer_name = "No writer mentioned"

        # Set article data
        article_data = {
            "writer": writer_name,
            "tags": ["N/A"],
            "content": content,
            "summary": summary,
            "image": image
        }

    # Catch exceptions
    except Exception:
        pass

    # Returns above defined default values if something goes wrong with scraping
    # Returns the actual values if everything goes well
    return article_data
