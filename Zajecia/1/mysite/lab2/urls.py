from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('osoby/', views.osoba_list, name='osoba-list'),
    path('osoby/<int:pk>/', views.osoba_detail, name='osoba-detail'),
    path('osoby/search/', views.osoba_search, name='osoba-search'),
    path('osoby/create/', views.osoba_create, name='osoba-create'),
    path('osoby/<int:pk>/update/', views.osoba_update, name='osoba-update'),
    path('osoby/<int:pk>/delete/', views.osoba_delete, name='osoba-delete'),
    path('stanowiska/', views.stanowisko_list, name='stanowisko-list'),
    path('stanowiska/<int:pk>/', views.stanowisko_detail, name='stanowisko-detail'),
    path('stanowiska/create/', views.stanowisko_create, name='stanowisko-create'),
    path('stanowiska/<int:pk>/update_delete/', views.stanowisko_update_delete, name='stanowisko-update-delete'),
    path('stanowisko/<int:pk>/members/', views.stanowisko_members, name='stanowisko-members'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
]