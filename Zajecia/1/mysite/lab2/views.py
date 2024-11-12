from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Osoba
from .serializers import OsobaSerializer

class OsobaList(APIView):
    """
    List all persons, or create a new person.
    """
    def get(self, request, format=None):
        osoby = Osoba.objects.all()
        serializer = OsobaSerializer(osoby, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OsobaDetail(APIView):
    """
    Retrieve, update or delete a person instance.
    """
    def get_object(self, pk):
        try:
            return Osoba.objects.get(pk=pk)
        except Osoba.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        osoba = self.get_object(pk)
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        osoba = self.get_object(pk)
        serializer = OsobaSerializer(osoba, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        osoba = self.get_object(pk)
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
