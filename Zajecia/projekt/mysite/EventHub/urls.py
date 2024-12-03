from django.urls import path
from .views import LoginView
from . import  views

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('users/', views.UserCRUD.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserCRUD.as_view(), name='user-detail'),

    path('events/', views.EventCRUD.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventCRUD.as_view(), name='event-detail'),

    path('enrollments/', views.EnrollmentCRUD.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', views.EnrollmentCRUD.as_view(), name='enrollment-detail'),

    path('comments/', views.CommentCRUD.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentCRUD.as_view(), name='comment-detail'),

    path('events/monthly-summary/', views.monthly_summary, name='monthly-summary'),
    path('events/top-rated/', views.top_rated, name='top-rated'),
    path('events/location/<str:city>/', views.events_by_location, name='events-by-location'),
    path('events/<int:id>/participants/', views.event_participants, name='event-participants'),
]