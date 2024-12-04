from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('osoby/', views.osoba_list, name='osoba_list'),
    path('osoby/<int:pk>/', views.osoba_detail, name='osoba_detail'),
    path('osoby/search/', views.osoba_search, name='osoba_search'),
    path('osoby/create/', views.osoba_create, name='osoba_create'),
    path('osoby/<int:pk>/update/', views.osoba_update, name='osoba_update'),
    path('osoby/<int:pk>/delete/', views.osoba_delete, name='osoba_delete'),
    path('osoba/<int:pk>/check-permission/', views.osoba_permission_check, name='osoba_permission_check'),
    path('stanowiska/', views.stanowisko_list, name='stanowisko_list'),
    path('stanowiska/<int:pk>/', views.stanowisko_detail, name='stanowisko_detail'),
    path('stanowiska/create/', views.stanowisko_create, name='stanowisko_create'),
    path('stanowiska/<int:pk>/update_delete/', views.stanowisko_update_delete, name='stanowisko_update_delete'),
    path('stanowisko/<int:pk>/members/', views.stanowisko_members, name='stanowisko_members'),
    #path('api-auth/', include('rest_framework.urls')),
    path('api/token-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
]