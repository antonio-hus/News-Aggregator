# Imports Section
# Python Libraries
import requests
from bs4 import BeautifulSoup


# Get article information from the given URL
def get(url):
    article_data = {
        "writer": 'Antonio Hus',
        "publish_date": '',
        "last_updated_date": '',
        "tags": [],
        "content": 'Currently Available only for DIGI24 Website',
    }

    return article_data
