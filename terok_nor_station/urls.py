"""terok_nor_station URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fan_database.views import index_view
from fan_database.views import season_view
from fan_database.views import add_episode
from fan_database.views import update_episode
from fan_database.views import delete_episode


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='Home'),
    path('season/<str:season_id>/episodes', season_view, name='Season'),
    path('add-episode/', add_episode, name='add-episode'),
    path('update-episode/<str:pk>/', update_episode, name='update-episode'),
    path('delete-episode/<str:pk>/', delete_episode, name='delete-episode'),
]
