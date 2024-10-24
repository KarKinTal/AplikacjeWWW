from rest_framework import serializers
from .models import Osoba, Team, Person, Stanowisko

class OsobaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    imie = serializers.CharField(max_length=50)
    nazwisko = serializers.CharField(max_length=50)
    plec = serializers.CharField(max_length=1)
    stanowisko = serializers.PrimaryKeyRelatedField(read_only=True)
    data_dodania = serializers.DateField(read_only=True)

    def create(self, validated_data):
        """
        Tworzy i zwraca nową instancję Osoba na podstawie zweryfikowanych danych.
        """
        return Osoba.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Aktualizuje i zwraca istniejącą instancję Osoba na podstawie zweryfikowanych danych.
        """
        instance.imie = validated_data.get('imie', instance.imie)
        instance.nazwisko = validated_data.get('nazwisko', instance.nazwisko)
        instance.plec = validated_data.get('plec', instance.plec)
        instance.stanowisko = validated_data.get('stanowisko', instance.stanowisko)
        instance.save()
        return instance


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class StanowiskoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = '__all__'