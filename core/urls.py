# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('preferences/', views.set_preferences, name='set_preferences'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('reading-list/', views.reading_list, name='reading_list'),
]