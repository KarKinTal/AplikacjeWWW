from django.db import models
from datetime import date
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
# deklaracja statycznej listy wyboru do wykorzystania w klasie modelu
MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')
BODY_TYPES = models.TextChoices('Typ sylwetki', 'Klepsydra Gruszka Jabłko Prostokąt Trójkąt')

SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )


class Team(models.Model):
    name = models.CharField(max_length=60)
    country = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):

    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)
    body_type = models.CharField(max_length=10, choices=BODY_TYPES.choices, default=BODY_TYPES['Jabłko'])

    def __str__(self):
        return self.name


PLEC_CHOICES = [
    ('K', 'Kobieta'),
    ('M', 'Mężczyzna'),
    ('I', 'Inne'),
]

class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=100, blank=False, null=False)
    opis = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nazwa


class Osoba(models.Model):
    class PlecChoices(models.IntegerChoices):
        KOBIETA = 1, 'Kobieta'
        MEZCZYZNA = 2, 'Mężczyzna'
        INNE = 3, 'Inne'

    imie = models.CharField(
        max_length=50,
        validators=[RegexValidator(regex=r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$', message="Imię może zawierać tylko litery.")],
        blank=False, null=False
    )
    nazwisko = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=r'^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$', message="Nazwisko może zawierać tylko litery.")],
        blank=False, null=False
    )
    plec = models.IntegerField(choices=PlecChoices.choices, default=PlecChoices.KOBIETA)
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.SET_NULL, null=True, blank=True)
    data_dodania = models.DateField(default=now)
    wlasciciel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='osoby', null=True, blank=True)

    class Meta:
        ordering = ['nazwisko']
        permissions = [
            ("can_view_other_persons", "Can view persons owned by other users"),
        ]

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"

    def clean(self):
        # Walidacja daty dodania
        if self.data_dodania and self.data_dodania > date.today():
            raise ValidationError("Data dodania nie może być w przyszłości.")
