from django.contrib import admin

from .models import Person, Team, Stanowisko, Osoba

admin.site.register(Person)
admin.site.register(Team)

class OsobaAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'stanowisko', 'stanowisko_new_name']
    readonly_fields = ['data_dodania']
    list_filter = ['stanowisko', 'data_dodania']

    def stanowisko_new_name(self, obj):
        if obj.stanowisko:
            return f"{obj.stanowisko.nazwa} ({obj.stanowisko.id})"
        return "Brak stanowiska"


class StanowiskoAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'opis']
    list_filter = ['nazwa']

admin.site.register(Osoba, OsobaAdmin)
admin.site.register(Stanowisko, StanowiskoAdmin)
# Register your models here.
