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
        article = BeautifulSoup(response.content, 'html.parser')

        # Extracting media
        image = ""
        image_div = article.find('div', class_='article--media')
        if image_div:
            image = image_div.find('img')['src'] \
                if image_div.find('img') else "No Media Found"

        # Finding main content
        content_div = article.find('div', class_='article--text')
        paragraphs = content_div.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]
        content = '\n'.join(article_content[:-4]) if article_content else "Content not found."

        # Extracting writer
        writer = article.find('div', class_="author--name").find('a')
        if writer:
            writer_name = writer.text.strip()
        else:
            writer_name = "No writer mentioned"

        # Extracting Category
        category = article.find('div', class_="article--section-information").find('a')
        if category:
            category_title = category.text.strip()
        else:
            category_title = "N/A"

        # Extract tags
        tags = [tag.get_text().strip() for tag in article.find_all('a', class_="article__info__tags_a")]

        # Set article data
        article_data = {
            "writer": writer_name,
            "tags": tags,
            "content": content,
            "category": category_title,
            "image": image,
        }

    # Catch exceptions
    except Exception:
        pass

    # Returns above defined default values if something goes wrong with scraping
    # Returns the actual values if everything goes well
    return article_data
