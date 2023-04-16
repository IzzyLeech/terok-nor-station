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
    path('approve_edit_request_confirm/<int:pk>/', views.approve_edit_request_confirm, name='approve_edit_request_confirm'),
    path('reject_edit_request_confirm/<int:pk>/', views.reject_edit_request_confirm, name='reject_edit_request_confirm'),
    path('search-query/', views.search_query, name='search-query'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.login_view, name='login'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),
    path('password_change_form/', views.password_change_form, name='password_change_form'),
    path('password_reset_form/', views.password_reset_form, name='password_reset_form'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
]

handler404 = 'fan_database.views.error_404'
