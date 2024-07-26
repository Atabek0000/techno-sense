from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('o_nas/', views.o_nas, name='o_nas'),
    path('weather_news/', views.weather_news, name='weather_news'),
    path('Documentation/', views.Documentation, name='Documentation'),

    path('progress/', views.progress_list, name='progress_list'),
    path('create/', views.progress_create, name='progress_create'),
    path('update/<int:pk>/', views.progress_update, name='progress_update'),
    path('news/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/update/<int:pk>/', views.news_update, name='news_update'),
]