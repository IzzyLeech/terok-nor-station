from django.urls import path
from . import views

urlpatterns = [
    path('community/', views.community_view, name='community'),
    path('create-post/', views.create_post, name='create-post'),
    path('post/', views.view_post, name='post'),
]
