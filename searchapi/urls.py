from django.urls import path
from searchapi import views

urlpatterns = [
    path('users/', views.index, name='index'),
    path('all/', views.fetch_all, name='index'),
]