from django.contrib import admin

from .models import Person
from .models import Team

admin.site.register(Person)
admin.site.register(Team)
# Register your models here.
