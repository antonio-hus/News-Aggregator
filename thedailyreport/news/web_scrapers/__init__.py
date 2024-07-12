"""

!!! Attention !!!
The scrape_news method shall return a list of article information in JSON form
This information will be used to initialize the Article Object

Example Below:

{
    "header_data": {
        "title_hash": "example_title_hash",
        "content_hash": "example_content_hash",
        "media_hash": "example_media_hash",
        "publish_date": "2023-07-12 12:34:56",
        "last_updated_date": "2023-07-12 12:34:56"
    },
    "article_information_data": {
        "writer": "John Doe",
        "tags": [
            {
                "id": 1,
                "name": "Technology"
            },
            {
                "id": 2,
                "name": "Science"
            }
        ],
        "categories": [
            {
                "id": 1,
                "name": "Tech News"
            },
            {
                "id": 2,
                "name": "Research"
            }
        ]
    },
    "article_preview_information": {
        "title_preview": "This is a preview title",
        "content_preview": "This is a preview of the content.",
        "media_preview": {
            "id": 1,
            "url": "https://example.com/media/preview.jpg"
        }
    },
    "article_content_information": {
        "title_full": "This is the full title",
        "content_full": "This is the full content of the article.",
        "medias_full": [
            {
                "id": 2,
                "url": "https://example.com/media/full1.jpg"
            },
            {
                "id": 3,
                "url": "https://example.com/media/full2.jpg"
            }
        ]
    },
    "article_mailing_information": {
        "title_mailing": "This is the mailing title",
        "content_mailing": "This is the mailing content of the article.",
        "medias_mailing": [
            {
                "id": 4,
                "url": "https://example.com/media/mailing1.jpg"
            },
            {
                "id": 5,
                "url": "https://example.com/media/mailing2.jpg"
            }
        ]
    },
    "news_source": {
        "publisher": {
            "id": 1,
            "name": "Example News Source"
        }
    }
}

"""