# Imports Section
from django.urls import path
from . import views

# API Endpoints
urlpatterns = [

    # User Related Endpoints
    path('user/', views.get_user, name='get_user'),

    # Articles Related Endpoints
    path('articles_all/', views.get_all_news, name='get_articles_all'),
    path('articles_following/', views.get_following_news, name='get_articles_following'),
    path('articles_publisher/<str:name>', views.get_publisher_news, name='get_articles_publisher'),
    path('articles_category/<str:title>', views.get_category_news, name='get_articles_category'),
    path('articles_tag/<str:title>', views.get_tagged_news, name='get_articles_tag'),

    # Authentication Endpoints
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
]
