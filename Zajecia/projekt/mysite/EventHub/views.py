from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth
from rest_framework import status
from .models import User, Event, Enrollment, Comment, Category
from .serializers import (
    UserSerializer, EventSerializer, EnrollmentSerializer, CommentSerializer, CategorySerializer, LoginSerializer
)


DEFAULT_AUTHENTICATION_CLASSES = [TokenAuthentication]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


# Rejestracja użytkownika
@api_view(['POST'])
@authentication_classes(DEFAULT_AUTHENTICATION_CLASSES)
@permission_classes([])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes(DEFAULT_AUTHENTICATION_CLASSES)
@permission_classes([])
def login(request):
    return Response({"detail": "Logowanie odbywa się przez TokenAuthentication lub inne metody standardowe."})



class UserCRUD(APIView):
    authentication_classes = DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class EventCRUD(APIView):
    authentication_classes = DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [IsAdminUser]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class EnrollmentCRUD(APIView):
    authentication_classes = DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(user=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk, user=request.user)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentCRUD(APIView):
    authentication_classes = DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.filter(user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Zestawienie miesięczne wydarzeń
@api_view(['GET'])
@authentication_classes(DEFAULT_AUTHENTICATION_CLASSES)
@permission_classes([IsAdminUser])
def monthly_summary(request):
    summary = (
        Event.objects.annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(event_count=Count('id'), participant_count=Count('enrollment__id'))
    )
    return Response(summary)



@api_view(['GET'])
@authentication_classes(DEFAULT_AUTHENTICATION_CLASSES)
@permission_classes([])
def top_rated(request):
    events = Event.objects.annotate(average_rating=Avg('comments__rating')).order_by('-average_rating')[:10]
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes(DEFAULT_AUTHENTICATION_CLASSES)
@permission_classes([])
def events_by_location(request, city):
    events = Event.objects.filter(location__icontains=city)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes(DEFAULT_AUTHENTICATION_CLASSES)
@permission_classes([IsAdminUser])
def event_participants(request, id):
    event = get_object_or_404(Event, pk=id)
    participants = Enrollment.objects.filter(event=event).select_related('user')
    serializer = UserSerializer([enrollment.user for enrollment in participants], many=True)
    return Response(serializer.data)