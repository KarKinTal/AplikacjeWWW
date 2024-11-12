from django.urls import path
from . import views

urlpatterns = [
    path('osoby/', views.OsobaList.as_view(), name='osoba-list'),
    path('osoby/<int:pk>/', views.OsobaDetail.as_view(), name='osoba-detail'),
]