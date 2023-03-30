from django.urls import path
from . import views

urlpatterns = [
    path('community/', views.community_view, name='community')
]

