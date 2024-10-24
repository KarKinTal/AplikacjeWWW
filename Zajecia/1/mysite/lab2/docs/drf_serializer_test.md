# Testowanie serializerów w Django Rest Framework

## 1. Serializacja obiektu `Osoba`

```python
from lab2.models import Osoba
from lab2.serializers import OsobaSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# 1. Tworzenie nowej instancji klasy Osoba
osoba = Osoba(imie='Anna', nazwisko='Kowalska', plec=1)
osoba.save()

# 2. Inicjalizacja serializera
serializer = OsobaSerializer(osoba)
serializer.data
# Output: {'id': 7, 'imie': 'Anna', 'nazwisko': 'Kowalska', 'plec': 1, 'stanowisko': None}

# 3. Serializacja danych do formatu JSON
content = JSONRenderer().render(serializer.data)
content
# Output: b'{"id":7,"imie":"Anna","nazwisko":"Kowalska","plec":1,"stanowisko":null}'

# Deserializacja danych
import io
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

deserializer = OsobaSerializer(data=data)
deserializer.is_valid()
# Output: True

deserializer.validated_data
# Output: OrderedDict([('imie', 'Anna'), ('nazwisko', 'Kowalska'), ('plec', 1), ('stanowisko', None)])

# Zapisanie danych po walidacji
deserializer.save()
# Output: <Osoba: Anna Kowalska>


from lab2.models import Stanowisko
from lab2.serializers import StanowiskoSerializer

# 1. Tworzenie nowej instancji klasy Stanowisko
stanowisko = Stanowisko(nazwa='Manager', opis='Zarządza zespołem')
stanowisko.save()

# 2. Serializacja danych modelu Stanowisko
serializer = StanowiskoSerializer(stanowisko)
serializer.data
# Output: {'id': 5, 'nazwa': 'Manager', 'opis': 'Zarządza zespołem'}

# Serializacja do formatu JSON
content = JSONRenderer().render(serializer.data)
content
# Output: b'{"id":5,"nazwa":"Manager","opis":"Zarządza zespołem"}'

# Deserializacja danych
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

deserializer = StanowiskoSerializer(data=data)
deserializer.is_valid()
# Output: True

deserializer.validated_data
# Output: OrderedDict([('nazwa', 'Manager'), ('opis', 'Zarządza zespołem')])

# Zapisanie danych po walidacji
deserializer.save()
# Output: <Stanowisko: Manager>