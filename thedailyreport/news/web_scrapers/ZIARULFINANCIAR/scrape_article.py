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
        "category": 'No category found',
        "summary": 'No summary found',
        "image": 'No image found'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('div', class_='article')
        if not article:
            return article_data

        # Extract category
        category_div = article.find('span', class_='underline')
        if category_div:
            category = category_div.find('span', class_='labelTag fleft').text.strip()
        else:
            category = 'N/A'

        # Extract main content
        paragraphs = article.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]

        # Extract summary
        summary = article_content[1]

        # Extract writer
        if 'Autor' in summary:
            summary = article_content[2]
            content = '\n'.join(article_content[2:-19]) if article_content else "Content not found."
        else:
            content = '\n'.join(article_content[1:-19]) if article_content else "Content not found."

        # Extract Image
        image = article.find('img')['src']
        image = 'https:' + image

        # Extract Writer
        writer_div = article.find('div', class_='author clear').find('a')
        if writer_div:
            writer_name = writer_div.text.strip()
        else:
            writer_name = "No writer mentioned"

        # Set article data
        article_data = {
            "writer": writer_name,
            "tags": ["N/A"],
            "content": content,
            "category": category,
            "summary": summary,
            "image": image
        }

    # Catch exceptions
    except Exception:
        pass

    # Returns above defined default values if something goes wrong with scraping
    # Returns the actual values if everything goes well
    return article_data