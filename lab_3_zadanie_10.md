from lab2.models import Osoba
osoby = Osoba.objects.all()
for osoba in osoby:
    print(osoba)
osoba_z_id_3 = Osoba.objects.get(id=3)
print(osoba_z_id_3)
osoby_na_litere = Osoba.objects.filter(nazwisko__startswith='P')
    print(osoba)
stanowiska = Osoba.objects.values_list('stanowisko__nazwa', flat=True).distinct()
for stanowisko in stanowiska:
    print(stanowisko)
stanowiska_sorted = Osoba.objects.values_list('stanowisko__nazwa', flat=True).order_by('-stanowisko__nazwa').distinct()
for stanowisko in stanowiska_sorted:
    print(stanowisko)
from lab2.models import Stanowisko
stanowisko = Stanowisko.objects.get(id=1)
nowa_osoba = Osoba(imie='Andrzelika', nazwisko='Dziura', stanowisko=stanowisko)
nowa_osoba.save()
print(nowa_osoba)