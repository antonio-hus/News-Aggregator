###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.urls import path
# Project Libraries
from . import views


################
# URL PATTERNS #
################
# Backend Patterns - API Endpoints
urlpatterns = [

    # USER ENDPOINTS
    # GET Endpoints
    path('user/', views.get_user, name='get_user'),
    path('user/profile/', views.get_user_data, name='get_user_data'),
    # POST/PUT Endpoints
    path('user/profile/update/', views.update_user_data, name='update_user_data'),

    # NEWS SOURCE ENDPOINTS
    # GET Endpoints
    path('get_publishers/', views.get_publishers, name='get_publishers'),
    path('publisher/<str:name>/', views.get_publisher_data, name='get_publisher_data'),
    # PUT/POST Endpoints
    path('publisher/<str:name>/follow/', views.follow_publisher, name='follow_publisher'),
    path('publisher/<str:name>/unfollow/', views.unfollow_publisher, name='unfollow_publisher'),

    # ARTICLE ENDPOINTS
    # GET Endpoints
    path('search/', views.search_articles, name='search_articles'),
    path('articles/<int:articleId>/', views.get_article, name='get_article'),
    path('articles_all/', views.get_all_news, name='get_articles_all'),
    path('articles_following/', views.get_following_news, name='get_articles_following'),
    path('articles_favorite/', views.get_favorite_news, name='get_favorite_news'),
    path('articles_read_later/', views.get_read_later_news, name='get_read_later_news'),
    path('articles_publisher/<str:name>/', views.get_publisher_news, name='get_articles_publisher'),
    path('articles_category/<str:title>/', views.get_category_news, name='get_articles_category'),
    path('articles_tag/<str:title>/', views.get_tagged_news, name='get_articles_tag'),
    # PUT/POST Endpoints
    path('articles/<int:articleId>/favorite', views.favorite_article, name='favorite_article'),
    path('articles/<int:articleId>/unfavorite', views.unfavorite_article, name='unfavorite_article'),
    path('articles/<int:articleId>/readlater', views.readlater_article, name='readlater_article'),
    path('articles/<int:articleId>/unreadlater', views.unreadlater_article, name='unreadlater_article'),

    # RECOMMENDATION SYSTEM ENDPOINTS
    # GET Endpoints
    path('collaborative_filter_articles/', views.recommend_articles_by_users, name='recommend_articles_by_users'),
    path('content_filter_articles/', views.recommend_articles_by_content, name='recommend_articles_by_content'),

    # AUTHENTICATION ENDPOINTS
    # PUT/POST Endpoints
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
]
