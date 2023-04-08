from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='Home'),
    path('season/<int:pk>/', views.season_view, name='Season'),
    path('episode/<int:episode_id>/', views.episode_view, name='Episode'),
    path('add-episode/', views.add_episode, name='add-episode'),
    path('update-episode/<str:pk>/', views.update_episode, name='update-episode'),
    path('delete-episode/<str:pk>/', views.delete_episode, name='delete-episode'),
    path('admin-request/', views.admin_request, name='admin-request'),
    path('delete-request/<int:pk>/approve/confirm/', views.approve_delete_request_confirm, name='approve_delete_request_confirm'),
    path('delete-request/<int:pk>/reject/confirm/', views.reject_delete_request_confirm, name='reject_delete_request_confirm'),
    path('add-request/<int:pk>/approve/confirm/', views.approve_add_request_confirm, name='approve_add_request_confirm'),
    path('add-request/<int:pk>/reject/confirm/', views.reject_add_request_confirm, name='reject_add_request_confirm'),
    path('search-query/', views.search_query, name='search-query'),
    path('sign-up/', views.sign_up, name='sign-up'),
]
