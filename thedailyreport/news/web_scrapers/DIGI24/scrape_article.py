# Imports Section
# Python Libraries
import requests
from bs4 import BeautifulSoup


# Gets article information from dig24 Website
def get(url):
    article_data = {}

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
            author_name = article_content[-2].replace("Editor : ", "").strip()
        else:
            # Author is not denoted by a p
            # Enlarge content
            content = content + "\n" + article_content[-2]

            # Extracting author
            author_tag = article.find('p', text=lambda x: x and " Editor : " in x)
            if author_tag:
                author_name = author_tag.text.replace(" Editor : ", "").strip()
            else:
                author_name = 'Author not found'

        # Extracting tags
        tags = [tag.get_text().strip() for tag in article.find_all('li', class_="tags-list-item") if "Etichete:" not in tag.get_text().strip()]

        article_data = {
            "writer": author_name,
            "publish_date": publish_date,
            "last_updated_date": last_updated_date,
            "tags": tags,
            "content": content,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing article: {e}")

    return article_data
