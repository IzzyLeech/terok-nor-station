from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='Home'),
    path('season/<int:pk>/', views.season_view, name='Season'),
    path('episode/<int:episode_id>/', views.episode_view, name='Episode'),
    path('add-episode/', views.add_episode, name='add-episode'),
    path('update-episode/<str:pk>/', views.update_episode, name='update-episode'),
    path('delete-episode/<str:pk>/', views.delete_episode, name='delete-episode'),
    path('delete-list-request/', views.delete_request_list, name='delete-request-list'),
    path('delete-requests/<int:pk>/approve/', views.approve_delete_request, name='approve_delete_request'),
    path('search-query/', views.search_query, name='search-query'),
    path('sign-up/', views.sign_up, name='sign-up'),
]
