from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Osoba, Stanowisko
from .serializers import OsobaSerializer, StanowiskoSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def osoba_list(request):
    if request.method == 'GET':
        osoby = Osoba.objects.filter(wlasciciel=request.user)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(wlasciciel=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def osoba_detail(request, pk):
    osoba = get_object_or_404(Osoba, pk=pk)
    serializer = OsobaSerializer(osoba)
    return Response(serializer.data)


@api_view(['PUT'])
def osoba_update(request, pk):
    """Edytuje istniejący obiekt Osoba (PUT)."""
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = OsobaSerializer(osoba, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def osoba_delete(request, pk):
    """Usuwa obiekt Osoba (DELETE)."""
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    osoba.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def osoba_create(request):
    serializer = OsobaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def osoba_search(request):
    query = request.query_params.get('q', None)
    if query:
        osoby = Osoba.objects.filter(imie__icontains=query)
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stanowisko_list(request):
    stanowiska = Stanowisko.objects.all()
    serializer = StanowiskoSerializer(stanowiska, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def stanowisko_detail(request, pk):
    stanowisko = get_object_or_404(Stanowisko, pk=pk)
    serializer = StanowiskoSerializer(stanowisko)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def stanowisko_create(request):
    serializer = StanowiskoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def stanowisko_update_delete(request, pk):
    stanowisko = get_object_or_404(Stanowisko, pk=pk)

    if request.method == 'PUT':
        serializer = StanowiskoSerializer(stanowisko, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def stanowisko_members(request, pk):
    """
    Wyświetla wszystkie osoby przypisane do danego stanowiska.
    """
    stanowisko = get_object_or_404(Stanowisko, pk=pk)

    osoby = Osoba.objects.filter(stanowisko=stanowisko)

    serializer = OsobaSerializer(osoby, many=True)
    return Response(serializer.data)
