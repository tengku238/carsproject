from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createcar/', views.createcar, name='createcar'),
    path('readcar/', views.readcar, name='readcar'),
    path('updatecar/', views.updatecar, name='updatecar'),
    path('deletecar/', views.deletecar, name='deletecar'),
    path('searchcar/', views.searchcar, name='searchcar'),
]
