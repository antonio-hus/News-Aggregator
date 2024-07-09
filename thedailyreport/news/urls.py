from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.get_user, name='get_user'),
    path('articles_all/', views.get_all_news, name='get_articles_all'),

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
]
