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
The app is structured in 4 main parts.
Besides those there are some Django App, Environment and Docker Configuration files.

1. **Backend**:  
The main Django App - Situated inside the news/ folder.  
The migrations/ folder contain the project's migrations.  
The webscrapers/ folder contain the handmade web scrapers built in Python dedicated to their website (found in the name of the scraper). Here the get_news method scrapes the preview data and get_article method
scrapes the article given by the url of the post.  
The admin.py file contains the Admin Screen Setup (this can be accessed via the /admin route).  
The apps.py file contains the App Configurations - in particular one that stands out is NewsConfig - which sends a signal when all apps are loaded and the background tasks can start working.
The models.py file define the Models of the web application - User, Media, Category, Tag, NewsSource, Article - with their respective fields, relations and methods (To be noted here are the hash fields
inside the Article structure that permit very fast queries and change detection).  
The serializers.py file define a JSON serialization method of all the models above.  
The signals.py file contains the signals sent out by NewsConfig (explained above).  
The tasks.py file define the background tasks which update the article database with newly scraped posts (note that they are atomic so they don't corupt data; also they are separate to be parallelized).  
The urls.py file define the endpoints of the API.  
The utils.py file define frequently used operations - logging methods, media handlers and database operations.  
The views.py file define the inner-workings of the API endpoints - with GET, PUT and POST operations - for either authenticated or unauthenticated viewers.  
   
2. **Frontend**:  
The frontend React.js App - Situated inside the frontend/ folder.  
The public/ folder contains metadata about the website (favicon, logo, manifest.json, robots.txt).
The src/ folder contains the React Components of the app.  
The StyleSheet.css defines the main stylesheet of the app.  
The index.js file defines the web HTML structure.  
The App.js file defines the most important component of the app - it contains a router to all other pages, and sets the layout of the site.  
The Articles/ folder contain all components that have to do with articles - basic - ArticleFeed, ArticleScreen - and generalizations - NewsFeeds, along with variations Search Feed and Publisher Feed which contain their respective additional information, as the name suggests.
The Authentication/ folder contain the authentication related components - login, register and logout - using Tokens (issued by the Django backend).
The Components/ folder contains the sidebar and disclaimer components.
The Errors/ folder contain the error screens (currently only 404-NotFound).
The Profiles/ folder contains the User (here the user can see and update its data) and Publisher Profiles (here the publisher contact information is shown along with a follow option and all its posts).  
The other files are React and Docker Configuration Files.
   
4. **Background**:  
Uses Celery, with a Redis Broker to queue background tasks.
Every 6 hours it triggers the tasks in tasks.py to run (only after all apps are loaded) - as defined in the celery.py file.
   
5. **Database**:  
Uses a Docker Image of PostgreSQL.  
It is only interacted with using the Django ORM.

## Technologies Used
- **Django**: Backend Framework used to develop a RESTful API to serve the frontend.
- **Python**: Used in pair with Django Framework and to build web scrapers using the BeautifulSoup Library.
- **Celery**: Task queue for handling background jobs ( scraping articles from media sources ) - allowed paralelization of tasks and reduced server downtime.
- **React.js**: Frontend Framework used to develop the webpage.
- **JavaScript**, **JSX**, **HTML**, **CSS**, **Bootstrap**: Used in pair with React.js Framework
- **Docker**: Containerization of the application.
- **PostgreSQL**: Database for storing data.

## License
This project is a personal endeavor and is not intended for public use or distribution. All rights are reserved by the author.
