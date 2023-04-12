from django.urls import path
from . import views

urlpatterns = [
    path('community/', views.community_view, name='community'),
    path('create-post/', views.create_post, name='create-post'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete-post'),
    path('post/<str:pk>/', views.view_post, name='post'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete-comment'),
    path('like/<int:pk>', views.like_view, name='like_post'),
]


handler404 = 'community.views.error_404'
