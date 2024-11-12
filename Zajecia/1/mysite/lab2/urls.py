from django.urls import path
from . import views

urlpatterns = [
    path('osoby/', views.osoba_list, name='osoba-list'),
    path('osoby/<int:pk>/', views.osoba_detail, name='osoba-detail'),
    path('osoby/search/', views.osoba_search, name='osoba-search'),
    path('stanowiska/', views.stanowisko_list, name='stanowisko-list'),
    path('stanowiska/<int:pk>/', views.stanowisko_detail, name='stanowisko-detail'),
]