# The Daily Report 

## Overview
The Daily Report is a web platform designed to aggregate news articles from multiple sources of Mass Media.
It offers users one place to stay up to date with all current events and opinions of multiple jurnalists.
The ultimate aim of this project is to present people with the necessary facts to be able to form an unbiased view of the world around us.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [License](#license)

## Installation
To run the News Aggregator locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/antonio-hus/News-Aggregator.git
    cd News-Aggregator/thedailyreport
    ```

2. Build and start the Docker containers:
    ```sh
    docker-compose up --build
    ```


## Usage
The website can be used without an account, but for the best experience i kindly suggest registering for one.
The application fetches the latest news articles ( every 6 hours ), and present them in an easily digestible format.
Users may also save articles to their favorite and/or read later lists. They may also follow liked news channels.
Browsing has been designed in such a way to allow those interested to find articles in the shortest time possible via 
the search route or filters both ascending and descending ( by publish date, category, tag, publisher, title ).
Moreover as they interact with posts, suggested articles will pop up by collaborative filtering ( favorited by similar users ),
or by content filtering ( from favorite article's category or tag ).

## Project Structure

## Technologies Used
- **Django**: Backend Framework used to develop a RESTful API to serve the frontend.
- **Python**: Used in pair with Django Framework and to build web scrapers using the BeautifulSoup Library.
- **Celery**: Task queue for handling background jobs ( scraping articles from media sources ) - allowed paralelization of tasks and reduced server downtime.
- **React.js**: Frontend Framework used to develop the webpage.
- **JavaScript**, **JSX**, **HTML**, **CSS**, **Bootstrap**: Used in pair with React.js Framework
- **Docker**: Containerization of the application.
- **PostgreSQL**: Database for storing data.

## License
