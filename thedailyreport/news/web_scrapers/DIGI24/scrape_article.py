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
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content of the page
        article = BeautifulSoup(response.content, 'html.parser')

        # Dates will be set to timezone.now()
        last_updated_date = ''
        publish_date = ''

        # Finding main content
        paragraphs = article.find_all('p')
        article_content = [paragraph.text.strip() for paragraph in paragraphs]
        content = '\n'.join(article_content[:-2]) if article_content else "Content not found."

        if "Editor : " in article_content[-2]:
            writer_name = article_content[-2].replace("Editor : ", "").strip()
        else:
            # writer is not denoted by a p
            # Enlarge content
            content = content + "\n" + article_content[-2]

            # Extracting writer
            writer_tag = article.find('p', text=lambda x: x and " Editor : " in x)
            if writer_tag:
                writer_name = writer_tag.text.replace(" Editor : ", "").strip()
            else:
                writer_name = 'writer not found'

        # Extract tags
        tags = [tag.get_text().strip() for tag in article.find_all('li', class_="tags-list-item") if "Etichete:" not in tag.get_text().strip()]

        # Set article data
        article_data = {
            "writer": writer_name,
            "tags": tags,
            "content": content,
        }

    # Catch exceptions
    except Exception:
        pass

    # Returns above defined default values if something goes wrong with scraping
    # Returns the actual values if everything goes well
    return article_data
