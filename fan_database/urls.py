from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='Home'),
    path('season/<str:season_id>/episodes', views.season_view, name='Season'),
    path('episode/<int:episode_id>/', views.episode_view, name='Episode'),
    path('add-episode/', views.add_episode, name='add-episode'),
    path('update-episode/<str:pk>/', views.update_episode, name='update-episode'),
    path('delete-episode/<str:pk>/', views.delete_episode, name='delete-episode'),
    path('search-query/', views.search_query, name='search-query'),
    path('sign-up/', views.sign_up, name='sign-up'),
]