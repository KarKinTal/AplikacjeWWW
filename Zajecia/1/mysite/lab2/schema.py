import graphene
from graphene_django import DjangoObjectType
from .models import Osoba, Stanowisko

class OsobaType(DjangoObjectType):
    class Meta:
        model = Osoba
        fields = ("id", "imie", "nazwisko", "plec", "stanowisko", "data_dodania", "wlasciciel")

class StanowiskoType(DjangoObjectType):
    class Meta:
        model = Stanowisko
        fields = ("id", "nazwa", "opis")


class Query(graphene.ObjectType):
    all_osoby = graphene.List(OsobaType)
    all_stanowiska = graphene.List(StanowiskoType)
    osoba_by_id = graphene.Field(OsobaType, id=graphene.Int(required=True))
    stanowisko_by_name = graphene.Field(StanowiskoType, nazwa=graphene.String(required=True))

    osoby_by_nazwisko_fragment = graphene.List(OsobaType, fragment=graphene.String(required=True))
    count_osoby_by_gender = graphene.Int(plec=graphene.Int(required=True))
    count_osoby_by_stanowisko = graphene.Int(stanowisko_id=graphene.Int(required=True))

    def resolve_all_osoby(root, info):
        return Osoba.objects.select_related("stanowisko").all()

    def resolve_all_stanowiska(root, info):
        return Stanowisko.objects.all()

    def resolve_osoba_by_id(root, info, id):
        try:
            return Osoba.objects.get(pk=id)
        except Osoba.DoesNotExist:
            raise Exception("Nie znaleziono osoby o podanym ID.")

    def resolve_stanowisko_by_name(root, info, nazwa):
        try:
            return Stanowisko.objects.get(nazwa=nazwa)
        except Stanowisko.DoesNotExist:
            raise Exception("Nie znaleziono stanowiska o podanej nazwie.")

    def resolve_osoby_by_nazwisko_fragment(root, info, fragment):
        return Osoba.objects.filter(nazwisko__icontains=fragment)

    def resolve_count_osoby_by_gender(root, info, plec):
        return Osoba.objects.filter(plec=plec).count()

    def resolve_count_osoby_by_stanowisko(root, info, stanowisko_id):
        return Osoba.objects.filter(stanowisko_id=stanowisko_id).count()

schema = graphene.Schema(query=Query)